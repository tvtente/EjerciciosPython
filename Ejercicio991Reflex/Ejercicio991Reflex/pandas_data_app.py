# Referencias cruzadas: ../Pandas_Reflex_paso_a_paso.ipynb; § indica el número de sección.
# El notebook incluye los rangos de líneas de esta versión; busca también los nombres si el archivo cambia.
import asyncio
import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation
from io import StringIO
from itertools import islice
from typing import Any, TypedDict

import pandas as pd
import reflex as rx
import reflex_xy as rxy


REGIONS = ["North", "South", "East", "West"]
MAX_CSV_BYTES = 2 * 1024 * 1024
MAX_ROWS = 10_000
UPLOAD_ID = "orders-csv"
# NOTEBOOK §1: ruta del CSV. En el cuaderno se localiza PROJECT antes de leer el mismo archivo.
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "orders.csv"
CSV_COLUMNS = ["region", "product", "units", "date", "unit_price", "unit_cost", "channel"]


class OrderRow(TypedDict):
    region: str
    product: str
    units: int
    date: str
    unit_price: float
    unit_cost: float
    channel: str


class RegionTotal(TypedDict):
    region: str
    units: int


class RegionColumns(TypedDict):
    region: list[str]
    units: list[int]


# NOTEBOOK §2: lectura y validación; el cuaderno reutiliza esta función, sin duplicar reglas.
def read_orders(data: bytes) -> list[OrderRow]:
    """Parse a bounded CSV and validate its columns and record values."""
    if len(data) > MAX_CSV_BYTES:
        raise ValueError("Choose a CSV of at most 2 MiB.")
    try:
        reader = csv.reader(
            StringIO(data.decode("utf-8-sig"), newline=""), strict=True
        )
        nonempty_rows = (row for row in reader if row)
        columns = next(nonempty_rows, [])
        rows = list(islice(nonempty_rows, MAX_ROWS + 1))
    except (UnicodeDecodeError, csv.Error) as error:
        raise ValueError(
            "Choose a valid UTF-8 CSV with three columns per row."
        ) from error
    if not columns or not rows:
        raise ValueError("The CSV needs a header and at least one record.")
    if columns not in (["region", "product", "units"], CSV_COLUMNS):
        raise ValueError("Usa region,product,units o el formato ampliado de data/orders.csv.")
    if len(rows) > MAX_ROWS:
        raise ValueError("Include between 1 and 10,000 records.")
    if any(len(row) != len(columns) for row in rows):
        raise ValueError("Cada fila debe tener el mismo número de columnas que la cabecera.")
    frame = pd.DataFrame(rows, columns=columns)
    frame["region"] = frame["region"].str.strip()
    frame["product"] = frame["product"].str.strip()
    frame["units"] = frame["units"].str.strip()
    if not frame["region"].isin(REGIONS).all():
        raise ValueError("Regions must be North, South, East, or West.")
    if not frame["product"].str.len().between(1, 80).all():
        raise ValueError("Each product must contain 1–80 characters.")
    if not frame["units"].str.fullmatch(r"[0-9]{1,7}").all():
        raise ValueError("Units must be whole numbers from 0 to 1,000,000.")
    frame["units"] = pd.to_numeric(frame["units"])
    if not frame["units"].between(0, 1_000_000).all():
        raise ValueError("Units must be whole numbers from 0 to 1,000,000.")
    # Compatibilidad con los CSV originales de tres columnas.
    # Sin fecha, precio o coste no inventamos ingresos ni series temporales.
    if columns == ["region", "product", "units"]:
        frame["date"] = ""
        frame["unit_price"] = 0.0
        frame["unit_cost"] = 0.0
        frame["channel"] = "Unknown"
    else:
        dates = pd.to_datetime(frame["date"], format="%Y-%m-%d", errors="coerce")
        if dates.isna().any():
            raise ValueError("Las fechas deben ser válidas y tener formato YYYY-MM-DD.")
        frame["date"] = dates.dt.strftime("%Y-%m-%d")
        for column in ["unit_price", "unit_cost"]:
            def parse_money(value):
                try:
                    number = Decimal(str(value).strip())
                    if not number.is_finite() or not 0 <= number <= 1_000_000:
                        raise ValueError
                    if number != number.quantize(Decimal("0.01")):
                        raise ValueError
                    return float(number)
                except (InvalidOperation, ValueError):
                    raise ValueError("Precios y costes: entre 0 y 1.000.000, con máximo dos decimales.")
            frame[column] = frame[column].map(parse_money)
        frame["channel"] = frame["channel"].str.strip()
        if not frame["channel"].isin(["Online", "Store", "Wholesale"]).all():
            raise ValueError("Canales permitidos: Online, Store, Wholesale.")
    return frame.to_dict(orient="records")


# NOTEBOOK §4 y §6: filtros con .loc y resumen de unidades por región.
def analyze_orders(
    records: list[OrderRow], region: str, product: str
) -> tuple[list[OrderRow], list[RegionTotal], int, int]:
    """Filter records and return a bounded preview plus complete aggregates."""
    frame = pd.DataFrame(records)
    if frame.empty:
        return [], [], 0, 0
    if region != "All":
        frame = frame.loc[frame["region"] == region]
    matches = frame.loc[
        frame["product"].str.contains(product.strip(), case=False, regex=False)
    ]
    summary = matches.groupby("region", as_index=False, sort=True)[
        "units"
    ].sum()
    return (
        matches.head(50).to_dict(orient="records"),
        summary.to_dict(orient="records"),
        len(matches),
        int(matches["units"].sum()),
    )


class PandasAppState(rx.State):
    _orders: list[OrderRow] = []
    rows: list[OrderRow] = []
    summary: list[RegionTotal] = []
    monthly: list[dict[str, Any]] = []
    products: list[dict[str, Any]] = []
    channels: list[dict[str, Any]] = []
    revenue: str = "0.00 €"
    profit: str = "0.00 €"
    region: str = "All"
    product: str = ""
    matching_count: int = 0
    total_units: int = 0
    loaded_count: int = 0
    processing: bool = False
    error: str = ""

    # NOTEBOOK §4–§6 y §8: filtros, importes, agrupaciones y conversión a listas de diccionarios.
    def _refresh(self):
        """Apply the current filter to the session's backend-only records."""
        self.rows, self.summary, self.matching_count, self.total_units = (
            analyze_orders(self._orders, self.region, self.product)
        )
        self.loaded_count = len(self._orders)
        # Todos los resúmenes usan TODOS los registros filtrados, no las 50 filas de vista previa.
        frame = pd.DataFrame(self._orders)
        self.monthly, self.products, self.channels = [], [], []
        self.revenue, self.profit = "0.00 €", "0.00 €"
        if frame.empty:
            return
        if self.region != "All":
            frame = frame.loc[frame["region"] == self.region]
        frame = frame.loc[frame["product"].str.contains(self.product.strip(), case=False, regex=False)].copy()
        # Calculamos en céntimos enteros antes de agregar para evitar errores monetarios.
        frame["revenue_cents"] = frame["units"] * frame["unit_price"].map(lambda x: round(x * 100))
        frame["profit_cents"] = frame["revenue_cents"] - frame["units"] * frame["unit_cost"].map(lambda x: round(x * 100))
        self.revenue = f"{frame['revenue_cents'].sum() / 100:.2f} €"
        self.profit = f"{frame['profit_cents'].sum() / 100:.2f} €"
        frame["month"] = frame["date"].str[:7]
        monthly = frame.loc[frame["month"] != ""].groupby("month", as_index=False)[["revenue_cents", "profit_cents"]].sum()
        monthly["revenue"] = monthly["revenue_cents"] / 100
        monthly["profit"] = monthly["profit_cents"] / 100
        self.monthly = monthly[["month", "revenue", "profit"]].to_dict("records")
        products = frame.groupby("product", as_index=False)["units"].sum()
        self.products = products.to_dict("records")
        channels = frame.groupby("channel", as_index=False)["revenue_cents"].sum()
        channels["revenue"] = channels["revenue_cents"] / 100
        self.channels = channels[["channel", "revenue"]].to_dict("records")

    @rx.event
    # NOTEBOOK §2 y §9: carga del archivo y comprobación del estado real de Reflex.
    def load_sample(self, clear_upload: bool = True):
        """Replace the dataset while retaining the applied filter."""
        if self.processing:
            return
        try:
            with DATA_PATH.open("rb") as source:
                self._orders = read_orders(source.read(MAX_CSV_BYTES + 1))
        except (OSError, ValueError) as error:
            self.error = f"No se pudo cargar data/orders.csv: {error}"
            return
        self.error = ""
        self._refresh()
        if clear_upload:
            return rx.clear_selected_files(UPLOAD_ID)

    @rx.event
    async def upload_csv(self, files: list[rx.UploadFile]):
        """Read and parse one bounded upload, clearing stale data on failure."""
        if self.processing:
            return
        self._orders = []
        self._refresh()
        self.error = ""
        if len(files) != 1:
            self.error = "Choose one CSV file."
            return
        self.processing = True
        yield
        try:
            data = await files[0].read(MAX_CSV_BYTES + 1)
            self._orders = await asyncio.to_thread(read_orders, data)
        except ValueError as error:
            self.error = str(error)
        except OSError:
            self.error = "The file could not be read. Please try again."
        finally:
            self.processing = False
            self._refresh()

    @rx.event
    # NOTEBOOK §3: region/product son variables allí; aquí llegan desde el formulario.
    def apply_filters(self, form_data: dict[str, Any]):
        """Apply a region and literal, case-insensitive product search."""
        if self.processing:
            return
        region = str(form_data.get("region", "All"))
        product = str(form_data.get("product", "")).strip()
        if region not in ["All", *REGIONS] or len(product) > 80:
            self.error = (
                "Choose a listed region and search with at most 80 characters."
            )
            return
        self.region = region
        self.product = product
        self.error = ""
        self._refresh()

    @rxy.data(cache=False)
    def region_data(self) -> RegionColumns:
        """Publish the complete filtered regional totals to the XY chart."""
        return {
            "region": [row["region"] for row in self.summary],
            "units": [row["units"] for row in self.summary],
        }

    @rx.event
    def download_summary(self):
        """Download the complete regional aggregate for the applied filter."""
        if self.processing or not self.summary:
            return
        csv = pd.DataFrame(self.summary, columns=["region", "units"]).to_csv(
            index=False
        )
        return rx.download(
            data=csv, filename="region-summary.csv", mime_type="text/csv"
        )


# NOTEBOOK §5: la tabla metrics representa aquí los indicadores de estas tarjetas.
def metric_card(label: str, value: rx.Var, icon: str):
    """Render one labelled aggregate alongside a decorative icon.

    Args:
        label: The metric's visible name.
        value: Its current state value.
        icon: The icon name.

    Returns:
        A card with a large numeric value.
    """
    return rx.box(
        rx.hstack(
            rx.text(label, size="2", color=rx.color("gray", 11)),
            rx.center(
                rx.icon(icon, size=17, aria_hidden=True),
                width="2rem",
                height="2rem",
                border_radius="10px",
                color=rx.color("violet", 11),
                background=rx.color("violet", 3),
            ),
            justify="between",
            width="100%",
        ),
        rx.text(value, size="8", weight="bold", letter_spacing="-0.04em"),
        width="100%",
        padding="1rem 1.25rem",
        background=rx.color("gray", 1),
        border=f"1px solid {rx.color('gray', 4)}",
        border_radius="14px",
        box_shadow="0 2px 6px rgba(0, 0, 0, 0.025)",
    )


# NOTEBOOK §7–§8: la interfaz muestra indicadores, gráfica regional y tabla de datos.
def pandas_data_app(show_upload: bool = True):
    """Render the order dashboard with optional local CSV upload controls.

    Args:
        show_upload: Include upload controls in the standalone app.

    Returns:
        Filters, metric cards, a chart, and matching records.
    """
    return rx.vstack(
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.icon(
                        "chart-no-axes-combined", size=14, aria_hidden=True
                    ),
                    rx.text(
                        "SALES ANALYTICS",
                        size="1",
                        weight="bold",
                        letter_spacing="0.12em",
                    ),
                    color=rx.color("violet", 11),
                    spacing="2",
                    align="center",
                ),
                rx.heading(
                    "Order explorer",
                    size="7",
                    as_="h2",
                    letter_spacing="-0.04em",
                ),
                rx.text(
                    "A closer look at your products and regions.",
                    size="2",
                    color=rx.color("gray", 11),
                ),
                spacing="2",
                align_items="start",
            ),
            rx.button(
                rx.icon("rotate-ccw", size=14, aria_hidden=True),
                "Cargar data/orders.csv",
                on_click=PandasAppState.load_sample(show_upload),
                disabled=PandasAppState.processing,
                variant="outline",
                color_scheme="gray",
                size="2",
                cursor="pointer",
            ),
            justify="between",
            align="start",
            gap="1rem",
            flex_wrap="wrap",
            width="100%",
        ),
        *(
            [
                rx.upload(
                    rx.vstack(
                        rx.text(
                            "Drop a CSV here or choose a file", weight="medium"
                        ),
                        rx.text("UTF-8 · up to 2 MiB · 10,000 rows", size="2"),
                        rx.foreach(
                            rx.selected_files(UPLOAD_ID),
                            lambda name: rx.text(name),
                        ),
                        spacing="2",
                    ),
                    id=UPLOAD_ID,
                    accept={"text/csv": [".csv"]},
                    multiple=False,
                    disabled=PandasAppState.processing,
                    width="100%",
                    padding="1.5rem",
                    border=f"1px dashed {rx.color('gray', 7)}",
                    border_radius="8px",
                    overflow_wrap="anywhere",
                ),
                rx.button(
                    "Load CSV",
                    on_click=PandasAppState.upload_csv(
                        rx.upload_files(upload_id=UPLOAD_ID)
                    ),
                    loading=PandasAppState.processing,
                    disabled=rx.selected_files(UPLOAD_ID).length() == 0,
                ),
            ]
            if show_upload
            else []
        ),
        rx.cond(
            PandasAppState.error != "",
            rx.text(
                PandasAppState.error, role="alert", color=rx.color("red", 11)
            ),
        ),
        rx.form(
            rx.grid(
                rx.vstack(
                    rx.el.label(
                        "Region",
                        html_for="order-region",
                        font_size="0.75rem",
                        font_weight="500",
                    ),
                    rx.el.select(
                        *[
                            rx.el.option(value, value=value)
                            for value in ["All", *REGIONS]
                        ],
                        id="order-region",
                        name="region",
                        default_value="All",
                        disabled=PandasAppState.processing,
                        padding="0.6rem 0.75rem",
                        height="40px",
                        width="100%",
                        min_width="0",
                        font_size="0.875rem",
                        border=f"1px solid {rx.color('gray', 7)}",
                        border_radius="8px",
                        background=rx.color("gray", 1),
                    ),
                    align_items="stretch",
                    min_width="0",
                    spacing="2",
                ),
                rx.vstack(
                    rx.el.label(
                        "Product contains",
                        html_for="order-product",
                        font_size="0.75rem",
                        font_weight="500",
                    ),
                    rx.input(
                        id="order-product",
                        name="product",
                        placeholder="Search products…",
                        width="100%",
                        min_width="0",
                        size="3",
                        max_length=80,
                        disabled=PandasAppState.processing,
                    ),
                    align_items="stretch",
                    min_width="0",
                    spacing="2",
                ),
                rx.button(
                    rx.icon("list-filter", size=16, aria_hidden=True),
                    "Apply filters",
                    type="submit",
                    color_scheme="violet",
                    cursor="pointer",
                    size="3",
                    align_self="end",
                    width="100%",
                    white_space="nowrap",
                    disabled=PandasAppState.processing,
                ),
                grid_template_columns="repeat(auto-fit, minmax(min(100%, 12rem), 1fr))",
                spacing="3",
                width="100%",
            ),
            on_submit=PandasAppState.apply_filters,
            width="100%",
            padding="1rem",
            background=rx.color("gray", 3),
            border_radius="12px",
        ),
        rx.callout("Datos ficticios · Filtra por región o producto: todas las gráficas e indicadores se actualizan juntos."),
        rx.grid(
            metric_card(
                "Matching orders", PandasAppState.matching_count, "rows-3"
            ),
            metric_card("Total units", PandasAppState.total_units, "package"),
            metric_card(
                "Records loaded", PandasAppState.loaded_count, "database"
            ),
            metric_card("Ingresos", PandasAppState.revenue, "euro"),
            metric_card("Beneficio bruto", PandasAppState.profit, "trending-up"),
            grid_template_columns="repeat(auto-fit, minmax(min(100%, 10rem), 1fr))",
            spacing="3",
            width="100%",
            role="status",
            aria_live="polite",
        ),
        rx.vstack(
            rx.flex(
                rx.vstack(
                    rx.heading("Units by region", size="4", as_="h3"),
                    rx.text(
                        "Unit totals across all matching orders.",
                        size="2",
                        color=rx.color("gray", 11),
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.button(
                    rx.icon("download", size=14, aria_hidden=True),
                    "Download summary",
                    on_click=PandasAppState.download_summary,
                    disabled=PandasAppState.processing
                    | (PandasAppState.matching_count == 0),
                    variant="soft",
                    color_scheme="violet",
                    size="2",
                    cursor="pointer",
                ),
                justify="between",
                align="start",
                flex_wrap="wrap",
                gap="0.75rem",
                width="100%",
            ),
            rx.cond(
                PandasAppState.matching_count > 0,
                rx.box(
                    # La gráfica lee el mismo resumen reactivo que las insignias.
                    # No necesita el canal binario ni el renderer de reflex_xy.
                    rx.recharts.bar_chart(
                        rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False),
                        rx.recharts.x_axis(data_key="region"),
                        rx.recharts.y_axis(allow_decimals=False),
                        rx.recharts.tooltip(),
                        rx.recharts.bar(data_key="units", fill="#6e56cf", name="Units"),
                        data=PandasAppState.summary,
                        width="100%",
                        height=280,
                    ),
                    width="100%",
                    min_width="0",
                    height="280px",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("search", size=24, color=rx.color("gray", 9)),
                        rx.text("No matching orders", weight="medium"),
                        rx.text(
                            "Load data or try a different region or product.",
                            size="2",
                        ),
                        align="center",
                    ),
                    min_height="200px",
                    background=rx.color("gray", 2),
                    border_radius="8px",
                ),
            ),
            rx.hstack(
                rx.foreach(
                    PandasAppState.summary,
                    lambda row: rx.badge(
                        row["region"],
                        ": ",
                        row["units"],
                        " units",
                        variant="soft",
                        size="2",
                    ),
                ),
                flex_wrap="wrap",
                gap="0.5rem",
                aria_label="Regional totals",
            ),
            spacing="4",
            align_items="stretch",
            padding=["1rem", "1.25rem"],
            background=rx.color("gray", 1),
            border=f"1px solid {rx.color('gray', 4)}",
            border_radius="14px",
            width="100%",
        ),
        extra_charts(),
        rx.vstack(
            rx.heading("Matching orders", size="4", as_="h3"),
            rx.text(
                "Up to 50 matching rows · totals include every match",
                size="2",
                color=rx.color("gray", 11),
            ),
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            *[
                                rx.table.column_header_cell(
                                    label,
                                    justify="end"
                                    if label == "Units"
                                    else "start",
                                )
                                for label in ["Region", "Product", "Units", "Fecha", "Precio (€)", "Coste (€)", "Canal"]
                            ]
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            PandasAppState.rows,
                            lambda row: rx.table.row(
                                rx.table.cell(
                                    rx.badge(
                                        row["region"],
                                        variant="soft",
                                        color_scheme="gray",
                                    )
                                ),
                                rx.table.cell(row["product"]),
                                rx.table.cell(
                                    row["units"],
                                    justify="end",
                                    font_variant_numeric="tabular-nums",
                                    font_weight="500",
                                ),
                                rx.table.cell(row["date"]),
                                rx.table.cell(row["unit_price"]),
                                rx.table.cell(row["unit_cost"]),
                                rx.table.cell(row["channel"]),
                            ),
                        )
                    ),
                    width="100%",
                ),
                width="100%",
                overflow_x="auto",
            ),
            rx.cond(
                PandasAppState.matching_count == 0,
                rx.text(
                    "No matching records. Load data or change the filters.",
                    size="2",
                ),
            ),
            spacing="4",
            align_items="stretch",
            padding=["1rem", "1.25rem"],
            background=rx.color("gray", 1),
            border=f"1px solid {rx.color('gray', 4)}",
            border_radius="14px",
            width="100%",
        ),
        spacing="5",
        align_items="stretch",
        width="100%",
        min_width="0",
        max_width="54rem",
        margin="0 auto",
        padding=["1rem", "1.5rem"],
        background=rx.color("gray", 2),
        border=f"1px solid {rx.color('gray', 4)}",
        border_radius="18px",
    )


def pandas_preview():
    """Show the same dashboard with sample data and no upload controls."""
    return rx.box(
        pandas_data_app(show_upload=False),
        on_mount=PandasAppState.load_sample(False),
        width="100%",
    )



# NOTEBOOK §7: mismas series, dibujadas con Matplotlib en el cuaderno y Recharts aquí.
def extra_charts():
    """Tres ejemplos: líneas temporales, barras por producto y barras por canal."""
    def card(title, explanation, chart):
        return rx.box(rx.heading(title, size="4"),
                      rx.text(explanation, size="2", color=rx.color("gray", 11), margin_y="12px"),
                      chart, width="100%", min_width="0", padding="20px",
                      background=rx.color("gray", 1), border_radius="14px")

    return rx.vstack(
        card("Ingresos y beneficio por mes",
             "groupby('month').sum(): ingresos = unidades × precio; beneficio bruto = ingresos − coste. Importes en euros, sin impuestos ni gastos adicionales.",
             rx.cond(PandasAppState.monthly.length() > 0,
                 rx.recharts.line_chart(
                     rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                     rx.recharts.x_axis(data_key="month"), rx.recharts.y_axis(),
                     rx.recharts.tooltip(), rx.recharts.legend(),
                     rx.recharts.line(data_key="revenue", name="Ingresos (€)", stroke="#6e56cf", stroke_width=3),
                     rx.recharts.line(data_key="profit", name="Beneficio (€)", stroke="#10b981", stroke_width=3),
                     data=PandasAppState.monthly, width="100%", height=300),
                 rx.text("Carga el CSV ampliado para ver la evolución mensual."))),
        card("Unidades por producto", "groupby('product')['units'].sum(): compara qué productos se venden más.",
             rx.recharts.bar_chart(
                 rx.recharts.x_axis(data_key="product"), rx.recharts.y_axis(allow_decimals=False),
                 rx.recharts.tooltip(), rx.recharts.bar(data_key="units", name="Unidades", fill="#38bdf8"),
                 data=PandasAppState.products, width="100%", height=260)),
        card("Ingresos por canal", "groupby('channel'): compara la facturación online, en tienda y mayorista.",
             rx.recharts.bar_chart(
                 rx.recharts.x_axis(data_key="channel"), rx.recharts.y_axis(),
                 rx.recharts.tooltip(), rx.recharts.bar(data_key="revenue", name="Ingresos (€)", fill="#f59e0b"),
                 data=PandasAppState.channels, width="100%", height=260)),
        rx.text("CSV antiguo de 3 columnas: sigue siendo válido; los ingresos se muestran como 0 y no hay fechas para la serie mensual.", size="1", color=rx.color("gray", 11)),
        width="100%", align="stretch", gap="20px",
    )
