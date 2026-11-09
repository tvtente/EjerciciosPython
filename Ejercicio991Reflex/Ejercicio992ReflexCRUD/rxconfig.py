"""Proyecto independiente: puertos distintos a los ejemplos de Ejercicio991Reflex."""
import reflex as rx

config = rx.Config(
    app_name='todo_app',
    frontend_port=3001,
    backend_port=8001,
    api_url='http://localhost:8001',
    deploy_url='http://localhost:3001',
    default_color_mode='dark',
    plugins=[rx.plugins.RadixThemesPlugin(
        theme=rx.theme(appearance='dark',accent_color='blue',panel_background='solid'))],
)
