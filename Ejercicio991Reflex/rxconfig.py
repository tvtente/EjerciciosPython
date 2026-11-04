import reflex as rx
import reflex_xy as rxy

config = rx.Config(
    app_name="Ejercicio991Reflex",
    frontend_packages=["@tailwindcss/postcss"],
    plugins=[rxy.XYPlugin()],
)