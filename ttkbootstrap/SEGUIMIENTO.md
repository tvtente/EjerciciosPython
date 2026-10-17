# Seguimiento del curso: interfaces y control de eventos

Última revisión: 9 de octubre de 2026.

## Alcance y comprobaciones

El repositorio reúne ejercicios independientes: Calculadora, POO, Excel,
ControlAsistencia, ProyectoControl, Ejercicio63 y otras carpetas numeradas.
Este seguimiento se centra en `ttkbootstrap`, donde continúa el trabajo de interfaces.
No se han reorganizado carpetas ni reformateado archivos Python.

Git estaba limpio al comenzar la revisión. Se comprobó la sintaxis de 15 archivos
Python y la estructura XML de 6 archivos `.ui` de esta carpeta. Un Python falla;
los seis XML se pueden analizar. Esto no equivale a probar sus interfaces ni sus
acciones. No se modificaron los registros JSON.

## Mapa del trabajo actual

| Archivo o grupo | Papel | Estado observado |
|---|---|---|
| `control_eventos.py` | Formulario base para comparar con Git | Métodos vacíos intencionadamente; conservar como referencia |
| `control_eventos_funcional.py` | Versión completa con Persona y JSON | Lógica implementada; referencia para añadir las acciones |
| `control_eventos_pyside6.py` | Versión equivalente con Qt | Lógica implementada; alternativa para aprender, no entrega literal de ttkbootstrap |
| `Ejercicio1Ttkboostrap.py` | Otra implementación del ejercicio de acceso | Usa una ruta JSON relativa al directorio desde el que se ejecuta |
| `app.py`, `app2.py`, `app2.ui` | Práctica de controles, temas y distribución | Diseño y código separados; el UI no ejecuta automáticamente las funciones del Python |
| `pygubu/eventos_pack.ui`, `pygubu/eventos_grid.ui`, `pygubu/eventos.ui` | Diseños visuales de eventos | XML válido; revisar qué diseño se elige como referencia antes de regenerar código |
| `pygubu/controleventos_uiui.py` | Interfaz codificada generada | Archivo de diseño generado |
| `pygubu/controleventos_ui.py` | Clase que hereda la interfaz anterior | Lugar para añadir acciones; actualmente solo inicializa la base |
| `pygubu/saludar.ui`, `pygubu/principalui.py`, `pygubu/principal.py` | Ejercicio de conexión de un botón | Arranque pendiente de corregir; acción vacía |
| `hola.ui`, `saludo.py` | Otra práctica de generación | El Python tiene un error de sintaxis |

Flujo para trabajar con Pygubu:

1. Editar el diseño `.ui` en el diseñador.
2. Generar o cargar la interfaz base.
3. Programar las acciones en la clase derivada, conservándolas fuera del archivo generado.
4. Ejecutar y verificar el resultado antes de registrar el avance en Git.

## Pendientes por prioridad

| Prioridad | Tarea | Evidencia y criterio de finalización |
|---|---|---|
| Alta | Corregir `saludo.py:77` | Falta una coma entre `text='button1'` y `command=...`; debe superar la comprobación de sintaxis y abrir |
| Alta | Corregir el arranque de `pygubu/principal.py` | `principalUI.__init__` exige `project_ui`, pero la clase derivada no lo pasa; debe cargar `saludar.ui` mediante una ruta basada en el archivo Python |
| Media | Conectar el saludo en `principal.py` | Implementar la acción vacía y comprobar que el botón lee el nombre y responde; verificar también la conexión del callback del Builder |
| Media | Revisar el diálogo de `app2.py:21` | Usa `ttk.Toplevel(app)`; comprobar la firma instalada y emplear `master=app` si corresponde, como en el control de eventos |
| Media | Elegir un diseño de eventos para continuar | Mantener las variantes didácticas, pero identificar qué `.ui` se modifica y qué clase ejecuta sus acciones |
| Media | Actualizar `README.md` | Aún describe `tema_personalizado/tema_personalizado.py`, que no está en el esquema actual |
| Baja | Unificar el criterio de rutas JSON | `Ejercicio1Ttkboostrap.py` usa `JSON_FILE = "asistentes.json"`; comprobar desde qué carpeta debe abrirse para no crear otro archivo por accidente |

## Próxima sesión propuesta

- [ ] Corregir y abrir el ejemplo de saludo.
- [ ] Conectar una única acción y explicar el recorrido botón → método → respuesta.
- [ ] Aplicar ese mismo recorrido al diseño de eventos elegido.
- [ ] Añadir registro y validaciones tomando la versión funcional como referencia.
- [ ] Añadir persistencia, búsqueda y contador; probar con un JSON temporal.

La base `control_eventos.py` permanece sin acciones hasta que se decida expresamente
trabajar sobre ella. Los `pass` de esa base no son fallos.

## Cómo registrar el avance

Al terminar una tarea, anotar aquí fecha, archivos cambiados, resultado comprobado
y siguiente paso. Marcar una tarea terminada solo tras verificar su comportamiento.
Revisar en Git únicamente los archivos de esa tarea y conservar espacios y sangría.
Evitar incluir asistentes reales en nuevos commits de ejercicios.

Comandos desde la raíz del curso:

```bash
git status --short
git diff -- ttkbootstrap
git diff --check
```

| Fecha | Avance | Verificación | Siguiente paso |
|---|---|---|---|
| 2026-10-09 | Inventario y revisión inicial | Sintaxis de 15 Python y XML de 6 UI; problemas anotados arriba | Corregir el ejemplo de saludo |

Este archivo es un registro manual de seguimiento; no ejecuta comprobaciones periódicas.
