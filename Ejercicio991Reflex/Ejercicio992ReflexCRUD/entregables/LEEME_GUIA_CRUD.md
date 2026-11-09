# Guía interactiva del CRUD

Abre **guia_crud_interactiva.html** con doble clic en un navegador. No hace falta internet, instalar paquetes ni arrancar Reflex.

## Explorar el código

1. Elige Crear, Leer, Editar, Completar, Eliminar o Inicializar.
2. Pulsa un nombre del diagrama para abrir su definición. Anterior y Siguiente recorren los mensajes en orden.
3. En el código, pulsa los nombres subrayados para seguir las llamadas entre archivos. El panel lateral explica la selección y muestra sus llamadas y referencias.
4. Las flechas superiores permiten volver a lo que estabas leyendo. La búsqueda localiza símbolos y coincidencias en el texto.
5. Puedes copiar una función, copiar el archivo entero o descargar el `.py`. Los números de línea también tienen enlaces.
6. «Ver la captura relacionada de la presentación» conserva la referencia visual original.

Los conceptos externos, como `session.commit()`, abren una explicación. La implementación de SQLModel o Reflex no forma parte del código incluido. Su enlace a la documentación oficial sí necesita internet.

## PowerPoint y HTML

**CRUD_Reflex_con_guia_HTML.pptx** conserva las 39 diapositivas y añade «Explorar código ↗». Cada enlace apunta a una sección de esta guía.

Mantén el PowerPoint y el HTML en la **misma carpeta**. Si los compartes, envía el ZIP y extráelo antes de abrirlo. Los enlaces locales pueden depender de los permisos del visor de presentaciones. Si el visor no abre un enlace, abre directamente el HTML.

## Actualizar el código incluido

La guía contiene una copia del código, no una conexión en tiempo real a los archivos. Desde la carpeta del proyecto:

```bash
python3 scripts/generar_guia_crud.py
```

Este comando analiza los cinco archivos Python, actualiza las definiciones, los números de línea y los enlaces y vuelve a generar `entregables/guia_crud_interactiva.html`. Utiliza la biblioteca estándar y no ejecuta la aplicación ni accede a la base de datos. Las explicaciones y los recorridos son material didáctico: revísalos si cambias el comportamiento del programa. Las capturas conservan la referencia de la presentación.

Para volver a añadir los enlaces HTML a una copia del PowerPoint:

```bash
python3 scripts/enlazar_guia_powerpoint.py
```

Fuentes de la guía: `docs/guia_crud.template.html`, `docs/guia_recorridos.json` y `docs/guia_assets/`.

## Comprobaciones

```bash
node tests/guide/check_guide.mjs
python3 tests/guide/check_source.py
```

Se comprueban los recorridos, enlaces, historial, búsqueda, copia exacta del código, portabilidad y fidelidad a los archivos. Las comprobaciones de JavaScript se ejecutan sin navegador. La herramienta de vista previa de esta sesión no permite abrir `file://`, por lo que no se ha verificado la apariencia o el comportamiento en un navegador real.
