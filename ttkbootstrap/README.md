# Aplicación con tema personalizado

Esta aplicación usa ttkbootstrap y carga su tema desde `json/my_themes.json`.
No necesita CSS.

Desde `/home/tvt/MEGA/EjerciciosPython`, con el entorno del curso
activado, ejecuta:

```bash
python3 tema_personalizado/tema_personalizado.py
```

También puedes elegir explícitamente el Python del entorno del curso:

```bash
/home/tvt/MEGA/EjerciciosPython/.venv/bin/python tema_personalizado.py
```

Este último comando se ejecuta desde la carpeta `tema_personalizado`.

## Prueba a cambiar los colores

- `bg`: fondo de la ventana.
- `fg`: texto general.
- `inputbg`: fondo del campo de texto.
- `success`: color del botón Saludar.
- `danger`: color del botón Salir.

Guarda el JSON y cierra y vuelve a ejecutar la aplicación para ver los cambios.
Los colores se escriben en hexadecimal, por ejemplo `#34d399`.
El nombre `custom_name` del JSON debe coincidir con `style.theme_use("custom_name")`.

En `tema_personalizado.py`, primero se crea `Window`, luego se obtiene `ventana.style`,
se carga el JSON y finalmente se aplica el tema. Así solo hay una ventana principal.
