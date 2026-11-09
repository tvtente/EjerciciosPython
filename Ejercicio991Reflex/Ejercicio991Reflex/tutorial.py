"""Aplicación didáctica: controles → eventos → estado → dashboard.

Los datos son de demostración y viven en el estado de la sesión, sin base de datos.
"""
from decimal import Decimal, InvalidOperation
import reflex as rx
from dataclasses import dataclass, replace

CATEGORIES = ["Formación", "Consultoría", "Soporte"]


@dataclass
class Sale:
    id: int
    client: str
    category: str
    cents: int
    paid: bool


def sample_sales() -> list[Sale]:
    return [
        Sale(id=1, client="Ana García", category="Formación", cents=12000, paid=True),
        Sale(id=2, client="Luis Martín", category="Consultoría", cents=35000, paid=False),
        Sale(id=3, client="Marta López", category="Soporte", cents=8500, paid=True),
    ]


class DashboardState(rx.State):
    """Una fuente de datos compartida por el formulario, la tabla y la gráfica."""
    sales: list[Sale] = sample_sales()
    next_id: int = 4
    search: str = ""
    category: str = "Todas"
    error: str = ""
    preview: str = ""
    confirmed: bool = False

    @rx.event
    def set_search(self, value: str):
        self.search = value

    @rx.event
    def set_category(self, value: str):
        self.category = value

    @rx.event
    def set_preview(self, value: str):
        self.preview = value

    @rx.event
    def set_confirmed(self, value: bool):
        self.confirmed = value

    @rx.var
    def visible_sales(self) -> list[Sale]:
        """Los filtros afectan tanto a la tabla como a los indicadores."""
        return [s for s in self.sales
                if self.search.casefold() in s.client.casefold()
                and (self.category == "Todas" or s.category == self.category)]

    @rx.var
    def total_count(self) -> int:
        return len(self.visible_sales)

    @rx.var
    def total(self) -> str:
        return f"{sum(s.cents for s in self.visible_sales) / 100:.2f} €"

    @rx.var
    def paid_total(self) -> str:
        return f"{sum(s.cents for s in self.visible_sales if s.paid) / 100:.2f} €"

    @rx.var
    def paid_percent(self) -> int:
        rows = self.visible_sales
        return round(100 * sum(s.paid for s in rows) / len(rows)) if rows else 0

    @rx.var
    def chart_data(self) -> list[dict[str, str | float]]:
        return [{"categoria": category,
                 "importe": sum(s.cents for s in self.visible_sales
                                if s.category == category) / 100}
                for category in CATEGORIES]

    @rx.event
    def save_sale(self, data: dict):
        """El formulario entrega los controles identificados por su atributo name."""
        client = str(data.get("client", "")).strip()
        category = str(data.get("category", ""))
        try:
            amount = Decimal(str(data.get("amount", "")).replace(",", "."))
            valid = amount.is_finite() and 0 < amount <= 1_000_000
            if not valid or amount != amount.quantize(Decimal("0.01")):
                raise ValueError
        except (InvalidOperation, ValueError):
            self.error = "Introduce un importe entre 0,01 y 1.000.000 €, con un máximo de dos decimales."
            return
        if len(client) < 2 or category not in CATEGORIES:
            self.error = "Escribe un cliente de al menos dos caracteres y selecciona una categoría."
            return
        self.sales = [*self.sales, Sale(id=self.next_id, client=client,
                      category=category, cents=int(amount * 100),
                      paid=data.get("paid") in (True, "on", "true"))]
        self.next_id += 1
        self.error = ""
        return rx.toast.success("Venta guardada. El dashboard ya está actualizado.")

    @rx.event
    def toggle_paid(self, sale_id: int):
        self.sales = [replace(s, paid=not s.paid) if s.id == sale_id else s
                      for s in self.sales]

    @rx.event
    def clear_sales(self):
        self.sales = []
        return rx.toast.info("Se han eliminado los registros de esta sesión.")

    @rx.event
    def restore_samples(self):
        self.sales = sample_sales()
        self.next_id = 4
        self.search = ""
        self.category = "Todas"
        self.error = ""
        return rx.toast.success("Datos de ejemplo restaurados.")


def panel(title: str, explanation: str, *children) -> rx.Component:
    """Componente reutilizable: contenido y estilos CSS compartidos."""
    return rx.box(
        rx.heading(title, size="5"),
        rx.text(explanation, color="#64748b", margin_top="8px", margin_bottom="20px"),
        *children, background_color="white", color="#0f172a", padding=["20px", "28px"],
        border="1px solid #e2e8f0", border_radius="18px", width="100%",
    )


def controls() -> rx.Component:
    return panel(
        "1 · Controles y mensajes",
        "on_change envía el valor al estado; Reflex actualiza la vista automáticamente.",
        rx.vstack(
            rx.text("Escribe tu nombre", weight="bold"),
            rx.input(placeholder="Por ejemplo, Elena", value=DashboardState.preview,
                     on_change=DashboardState.set_preview, width="100%"),
            rx.text("Vista previa: ", DashboardState.preview),
            rx.checkbox("He comprendido cómo funciona el estado",
                        checked=DashboardState.confirmed,
                        on_change=DashboardState.set_confirmed),
            rx.badge(rx.cond(DashboardState.confirmed, "¡Listo para continuar!", "Prueba los controles")),
            rx.flex(
                rx.button("Aviso breve", on_click=rx.toast.info("Este mensaje no bloquea la pantalla.")),
                rx.dialog.root(
                    rx.dialog.trigger(rx.button("Abrir mensaje", variant="soft")),
                    rx.dialog.content(
                        rx.dialog.title("Una caja de mensajes en Reflex"),
                        rx.dialog.description("Un diálogo muestra información y permite esperar a que el usuario lo cierre."),
                        rx.dialog.close(rx.button("Entendido", margin_top="20px")),
                    ),
                ), gap="12px", flex_wrap="wrap",
            ), align="start", gap="12px", width="100%",
        ),
    )


def sales_form() -> rx.Component:
    return panel(
        "2 · Formulario de ventas",
        "Cada name identifica un dato. on_submit valida y añade la venta al estado.",
        rx.form(
            rx.vstack(
                rx.text("Cliente", weight="bold"),
                rx.input(name="client", placeholder="Nombre del cliente", required=True, min_length=2, width="100%"),
                rx.text("Categoría", weight="bold"),
                rx.select(CATEGORIES, name="category", default_value="Formación", width="100%"),
                rx.text("Importe (€)", weight="bold"),
                rx.input(name="amount", type="number", min="0.01", max="1000000", step="0.01",
                         placeholder="125.50", required=True, width="100%"),
                rx.checkbox("Venta cobrada", name="paid"),
                rx.cond(DashboardState.error != "", rx.callout(DashboardState.error, color_scheme="red", role="alert")),
                rx.button("Guardar venta", type="submit", width="100%"),
                rx.text("Los campos se conservan para que puedas corregirlos o registrar otra venta.", size="2", color="#64748b"),
                gap="12px", align="start", width="100%",
            ), on_submit=DashboardState.save_sale, reset_on_submit=False,
        ),
    )


def metric(label: str, value) -> rx.Component:
    return rx.box(rx.text(label, size="2", color="#64748b"),
                  rx.heading(value, size="7", margin_top="8px"),
                  padding="20px", background_color="#f8fafc", border_radius="12px")


def sale_row(sale: rx.Var[Sale]) -> rx.Component:
    return rx.table.row(
        rx.table.cell(sale.client), rx.table.cell(sale.category),
        rx.table.cell((sale.cents / 100).to_string(), " €"),
        rx.table.cell(rx.badge(rx.cond(sale.paid, "Cobrada", "Pendiente"),
                              color_scheme=rx.cond(sale.paid, "green", "orange"))),
        rx.table.cell(rx.button(rx.cond(sale.paid, "Marcar pendiente", "Marcar cobrada"),
                                variant="soft", size="1",
                                on_click=DashboardState.toggle_paid(sale.id))),
    )


def dashboard() -> rx.Component:
    return panel(
        "3 · Dashboard en directo",
        "Busca o filtra: indicadores, gráfica y tabla utilizan las mismas ventas visibles.",
        rx.flex(
            rx.input(placeholder="Buscar cliente…", aria_label="Buscar cliente", value=DashboardState.search,
                     on_change=DashboardState.set_search),
            rx.select(["Todas", *CATEGORIES], value=DashboardState.category,
                      on_change=DashboardState.set_category, aria_label="Filtrar por categoría"),
            gap="12px", flex_wrap="wrap", margin_bottom="20px",
        ),
        rx.grid(metric("Ventas visibles", DashboardState.total_count),
                metric("Importe total", DashboardState.total),
                metric("Cobrado", DashboardState.paid_total),
                columns=rx.breakpoints(initial="1", sm="3"), gap="12px"),
        rx.text("Porcentaje de ventas cobradas: ", DashboardState.paid_percent, "%", margin_top="20px"),
        rx.progress(value=DashboardState.paid_percent, max=100, margin_top="8px"),
        rx.heading("Importe por categoría (€)", size="4", margin_top="28px"),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False),
            rx.recharts.x_axis(data_key="categoria"), rx.recharts.y_axis(),
            rx.recharts.tooltip(), rx.recharts.bar(data_key="importe", fill="#6366f1"),
            data=DashboardState.chart_data, width="100%", height=260,
        ),
        rx.cond(DashboardState.total_count > 0,
            rx.box(rx.table.root(
                rx.table.header(rx.table.row(*[rx.table.column_header_cell(t) for t in
                                               ["Cliente", "Categoría", "Importe", "Estado", "Acción"]])),
                rx.table.body(rx.foreach(DashboardState.visible_sales, sale_row)), width="100%"),
                overflow_x="auto"),
            rx.callout("No hay ventas con estos filtros. Añade una o cambia la búsqueda.")),
        rx.flex(
            rx.button("Restaurar ejemplos", variant="soft", on_click=DashboardState.restore_samples),
            rx.alert_dialog.root(
                rx.alert_dialog.trigger(rx.button("Borrar todas las ventas", color_scheme="red", variant="soft")),
                rx.alert_dialog.content(
                    rx.alert_dialog.title("¿Borrar todas las ventas?"),
                    rx.alert_dialog.description("Se borrarán todos los registros de esta sesión, incluidos los ocultos por los filtros."),
                    rx.flex(rx.alert_dialog.cancel(rx.button("Cancelar", variant="soft")),
                            rx.alert_dialog.action(rx.button("Sí, borrar", color_scheme="red", on_click=DashboardState.clear_sales)),
                            justify="end", gap="12px", margin_top="20px"),
                ),
            ), gap="12px", flex_wrap="wrap", margin_top="24px",
        ),
    )


def tutorial_index() -> rx.Component:
    return rx.box(
        rx.box(rx.vstack(
            rx.badge("REFLEX · APRENDE HACIENDO", color_scheme="indigo"),
            rx.heading("Tu primer panel de ventas", size="8"),
            rx.text("Controles, mensajes y formularios conectados a un dashboard real.", size="4", color="#cbd5e1"),
            rx.link("Ver mis ejercicios anteriores →", href="/ejemplos", color="#c7d2fe"),
            align="start", gap="12px"), background_color="#0f172a", color="white", padding="36px", border_radius="20px"),
        rx.callout("Datos de demostración por sesión: no hay base de datos. Usa información ficticia; los cambios no se guardan de forma permanente.", margin_top="20px"),
        rx.grid(controls(), sales_form(), columns=rx.breakpoints(initial="1", md="2"), gap="24px", margin_top="24px"),
        rx.box(dashboard(), margin_top="24px"),
        rx.box(panel("4 · Cómo funciona", "El recorrido de un dato, de principio a fin.",
            rx.ordered_list(
                rx.list.item("El usuario escribe en un control o envía el formulario."),
                rx.list.item("on_change / on_submit ejecutan un método marcado con @rx.event."),
                rx.list.item("El evento modifica DashboardState: es el estado de la aplicación."),
                rx.list.item("Las propiedades @rx.var recalculan filtros, totales y gráfica."),
                rx.list.item("Reflex actualiza los componentes que leen esos valores."),
                gap="10px",
            ), rx.text("Prueba: guarda una venta pendiente de 100 €, localízala y márcala como cobrada. Observa cómo cambian los indicadores.", margin_top="20px", weight="bold")), margin_top="24px"),
        max_width="1200px", margin="0 auto", padding=["16px", "32px"],
        background_color="#f1f5f9", min_height="100vh",
    )
