# o05 · Chat App

Abre http://localhost:3000/o05_chat_app. También tienes un enlace desde la portada del contador.

## Probar sin configurar nada

El modo **Demo local** funciona con respuestas predefinidas: no es una IA ni necesita red. Pregunta por Reflex, State, formularios o streaming. El texto aparece por fragmentos para estudiar el comportamiento.

Enviar o Enter inicia la respuesta. Detener conserva lo recibido hasta ese momento; Nueva conversación borra el historial de esta sesión. Mientras responde se bloquean los controles que podrían mezclar conversaciones. El historial no se guarda en una base de datos.

## Recorrido del código

En `Ejercicio991Reflex/o05_chat_app.py`:

1. `question` se conecta al input mediante value y on_change.
2. `answer` valida la pregunta y evita peticiones simultáneas.
3. El historial es una lista de parejas (pregunta, respuesta).
4. El evento se ejecuta en segundo plano. Los bloques `async with self` protegen cambios breves de estado; no se espera una respuesta de red dentro del bloqueo.
5. `response_chunks` produce texto. `yield` envía los cambios y desplaza la vista al final del historial.
6. `qa` dibuja una pareja; `chat` usa foreach; `action_bar` contiene el formulario.
7. `aclosing` cierra el generador y la conexión si el usuario detiene el texto.

El ejercicio permite 2000 caracteres por pregunta y 20 turnos. Cambiar entre Demo local y OpenAI inicia una conversación nueva para no enviar respuestas simuladas como contexto real.

## OpenAI opcional

La interfaz está preparada, pero este modo requiere instalar el SDK en el entorno de Reflex y configurar el servidor. No se hizo ninguna llamada real a la API durante la construcción ni las pruebas.

Desde Ejercicio991Reflex, con el entorno activado:

```bash
uv pip install --python ../.venv/bin/python openai
```

Define OPENAI_API_KEY en tu terminal o gestor de secretos, sin guardarla en el código ni compartirla por el chat. Opcionalmente define OPENAI_MODEL con un modelo al que tu proyecto tenga acceso. El ejemplo usa gpt-4o-mini por defecto, como el tutorial.

Reinicia Reflex y elige OpenAI en la página. Solo al enviar una pregunta se transmite el historial de esa conversación a la API; puede tener coste. La clave no se muestra ni se guarda en variables públicas del State.

La integración adapta el tutorial a Responses API: recibe eventos `response.output_text.delta`, limita la respuesta a 800 tokens de salida y establece `store=False`. Esto no equivale a una garantía de ausencia total de retención del proveedor. Un fallo elimina el turno incompleto y recupera la pregunta para reintentar. Detener solicita el cierre al recibir el siguiente fragmento; no garantiza cancelación inmediata durante una espera de red.

## Ejercicios

- Añade un tema a demo_response y observa cómo cambia la respuesta local.
- Modifica colores y anchuras en qa.
- Compara el primer yield (pregunta visible y campo limpio) con los siguientes (texto progresivo).
- Provoca una configuración incompleta de OpenAI y comprueba que el historial no recibe un turno vacío.
- Detén una respuesta y comprueba que puedes iniciar otra.

## Validación

Compilación de Reflex y seis pruebas pasan: historial, contexto, bloqueo de duplicados, errores, recuperación, límites, falta de clave y cierre al detener. El proveedor real y la apariencia en el navegador quedan pendientes de una prueba con configuración propia.

Referencias:
- https://reflex.dev/docs/getting-started/chatapp-tutorial/
- https://developers.openai.com/api/docs/guides/streaming-responses

## Ollama local (modo inicial)

El chat incorpora Ollama mediante la API nativa `/api/chat`. No requiere el SDK OpenAI ni una clave.

1. Asegúrate de que el servicio Ollama está en marcha.
2. Abre `/o05_chat_app` y selecciona **Ollama local** si tu sesión conservaba otro modo.
3. Pulsa **Actualizar modelos**; el catálogo se consulta también al entrar.
4. Selecciona el modelo y envía tu pregunta. Cambiar de modelo inicia una conversación nueva.

El servidor predeterminado es `http://127.0.0.1:11434`. La conexión se realiza desde Python: si Reflex se ejecuta en Docker u otra máquina, localhost se refiere a ese entorno. Puedes configurar OLLAMA_HOST en el servidor y reiniciar Reflex. No se requiere abrir Ollama a Internet ni cambiar CORS para esta aplicación local.

Tus modelos preferidos aparecen primero: novelista, novelista-qwen, directorporno y tavata-fanvue. También se detectan otros modelos instalados con capacidad completion. tavata-embeddings solo tiene capacidad embedding: se informa de él, pero no se ofrece como asistente conversacional.

El adaptador `ollama_chat.py` comprueba capacidades, lee JSON por línea y utiliza message.content como texto. El campo thinking no se presenta como respuesta. En modelos que anuncian thinking se solicita think=False para obtener la respuesta directa. Se limita la generación a 800 tokens y se mantiene el modelo cargado hasta cinco minutos. Una primera respuesta puede tardar más por la carga en memoria.

La petición incluye el historial y el modelo seleccionado. No se añade un mensaje system que sustituya el carácter de tus modelos personalizados. El servicio y los pesos son los de tu instalación; esta integración llama a su dirección local y no a OpenAI.

Errores de conexión, modelos ausentes, embeddings o streams interrumpidos se muestran en español y recuperan la pregunta para reintentar. Detener cierra el stream al recibir el siguiente fragmento. Las pruebas automatizadas usan un servidor simulado, además de una comprobación separada de la conexión local real.

Referencia de la API: https://docs.ollama.com/api/chat
