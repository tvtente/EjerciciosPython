"""Contador visual con las clases y funciones de los ejercicios originales."""
import reflex as rx
from .tutorial import tutorial_index
from .pandas_data_app import pandas_data_app


class State(rx.State):
    count: int = 0
    color: str = "#4f46e5"

    @rx.event
    def increment(self, amount: int):
        self.count += amount

    @rx.event
    def decrement(self, amount: int):
        self.count -= amount

    @rx.event
    def reset_counter(self):
        self.count = 0
        return rx.toast.info("Contador reiniciado")

    @rx.var
    def progress(self) -> int:
        return max(0, min(100, self.count))


class TextState(rx.State):
    text: str = "Mi contador"

    @rx.event
    def update_text(self, new_text: str):
        self.text = new_text


def text_input():
    return rx.vstack(
        rx.text("NOMBRE DEL CONTADOR", size="1", weight="bold", color="#64748b", letter_spacing="0.12em"),
        rx.input(value=TextState.text, on_change=TextState.update_text,
                 placeholder="Ponle un nombre…", aria_label="Nombre del contador",
                 size="3", width="100%", max_length=60),
        gap="10px", align="start", width="100%",
    )


def check_even(num: int):
    return num % 2 == 0


class UsoPython(rx.State):
    count: int = 0
    text: str = "Par"

    @rx.event
    def increment(self):
        # Comprobamos el número después de incrementarlo.
        self.count += 1
        self.text = "Par" if check_even(self.count) else "Impar"


def count_and_check():
    return rx.vstack(
        rx.hstack(rx.icon("code", size=18), rx.text("Un poco de Python", weight="bold")),
        rx.text("Este contador independiente usa check_even() para distinguir pares e impares.", size="2", color="#64748b"),
        rx.hstack(rx.heading(UsoPython.count, size="6"), rx.badge(UsoPython.text), align="center", gap="12px"),
        rx.button("Probar siguiente número", on_click=UsoPython.increment, variant="soft"),
        align="start", gap="14px", padding="24px", background_color="#eef2ff", border_radius="18px", width="100%",
    )


def my_button():
    return rx.button(rx.icon("rotate-ccw", size=16), "Reiniciar contador",
                     on_click=State.reset_counter, variant="soft", color_scheme="gray", size="3")


def my_container():
    return rx.flex(
        rx.box(rx.text("Empieza de nuevo", weight="bold"), rx.text("Vuelve a cero cuando lo necesites.", size="2", color="#64748b")),
        my_button(), justify="between", align="center", flex_wrap="wrap", gap="16px",
        padding_top="24px", border_top="1px solid #e2e8f0", width="100%",
    )


def my_div():
    return rx.el.div(
        rx.el.p("Hecho con Python + Reflex · Cada clic cambia el estado y actualiza la pantalla."),
        color="#64748b", font_size="13px", text_align="center", padding="24px 0",
    )


def half_filled_progress():
    # Conservamos la función, pero ahora la barra muestra el progreso real.
    return rx.vstack(
        rx.flex(rx.text("Objetivo de práctica", size="2", weight="bold"), rx.text(State.progress, " / 100", size="2"), justify="between", width="100%"),
        rx.progress(value=State.progress, max=100, color_scheme="indigo", width="100%"),
        rx.text("La barra se limita a 0–100. El contador admite valores negativos y mayores que 100.", size="1", color="#64748b"),
        gap="10px", width="100%", align="start",
    )


def counter():
    return rx.vstack(
        rx.heading(rx.cond(TextState.text != "", TextState.text, "Mi contador"), size="5", color="#475569", text_align="center", overflow_wrap="anywhere"),
        rx.heading(State.count, as_="h1", font_size=["72px", "104px"], line_height="1.1", color=State.color,
                   letter_spacing="-0.06em", font_variant_numeric="tabular-nums", aria_live="polite"),
        rx.badge(rx.cond(State.count >= 0, "Sigue sumando", "También puedes contar en negativo"), color_scheme="indigo"),
        align="center", gap="14px", padding="28px 0", width="100%",
    )


def counter_variable():
    return rx.flex(
        rx.button(rx.icon("minus", size=18), "Restar 1", on_click=State.decrement(1), variant="outline", color_scheme="indigo", size="3"),
        rx.button(rx.icon("plus", size=18), "Sumar 1", on_click=State.increment(1), color_scheme="indigo", size="3"),
        rx.button("+5", on_click=State.increment(5), variant="soft", color_scheme="indigo", size="3"),
        justify="center", flex_wrap="wrap", gap="12px", width="100%",
    )


def index():
    return rx.box(
        rx.box(
            rx.flex(
                rx.hstack(rx.box(rx.icon("hash", size=24, color="white"), background_color="#4f46e5", padding="12px", border_radius="14px"),
                          rx.box(rx.text("REFLEX LAB", size="1", weight="bold", color="#4f46e5", letter_spacing="0.15em"), rx.heading("Cada clic cuenta", size="7", color="#0f172a")), gap="14px", align="center"),
                rx.link("Dashboard de ventas ↗", href="/tutorial", color="#4f46e5"),
                justify="between", align="center", flex_wrap="wrap", gap="20px", margin_bottom="28px",
            ),
            rx.text("Explora controles, eventos y estado con tus ejemplos de siempre.", color="#64748b", margin_bottom="28px"),
            rx.grid(
                rx.vstack(text_input(), counter(), counter_variable(), half_filled_progress(), my_container(),
                          gap="28px", width="100%", background_color="white", padding=["24px", "36px"], border_radius="24px",
                          border="1px solid #e2e8f0", box_shadow="0 16px 48px rgba(15,23,42,0.05)"),
                rx.vstack(
                    count_and_check(),
                    rx.box(rx.heading("¿Qué está pasando?", size="4"),
                           rx.text("1. Los botones llaman a increment() o decrement().", margin_top="16px"),
                           rx.text("2. State guarda el nuevo valor de count.", margin_top="12px"),
                           rx.text("3. Reflex actualiza el número y la barra de progreso.", margin_top="12px"),
                           rx.callout("TextState guarda el nombre. UsoPython mantiene el contador de paridad independiente.", margin_top="20px", size="1"),
                           padding="24px", background_color="white", border="1px solid #e2e8f0", border_radius="18px", color="#475569"),
                    gap="20px", width="100%",
                ), columns=rx.breakpoints(initial="1", md="2"), gap="24px", align_items="start",
            ),
            my_div(), max_width="1080px", margin="0 auto",
        ), background_color="#f1f5f9", min_height="100vh", padding=["24px 16px", "48px 32px"],
    )


app = rx.App()
app.add_page(index, route="/", title="Cada clic cuenta · Reflex")
app.add_page(index, route="/ejemplos", title="Contador · Mis ejemplos")
app.add_page(tutorial_index, route="/tutorial", title="Aprende Reflex · Panel de ventas")
app.add_page(pandas_data_app, route="/pandas", title="Datos de Pandas · Reflex")