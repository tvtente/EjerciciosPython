import reflex as rx
import reflex_xy as rxy

config = rx.Config(
    app_name="Ejercicio991Reflex",
    default_color_mode="light",
    frontend_packages=["@tailwindcss/postcss"],
    plugins=[
        rxy.XYPlugin(),
        # Tarjetas blancas con tipografía oscura y paneles sólidos en todas las páginas.
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(appearance="light", accent_color="indigo", panel_background="solid"),
        ),
    ],
)
