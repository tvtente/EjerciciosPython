"""o05 · Chat didáctico: historial, eventos en segundo plano y texto progresivo.

Reflex Chatapp Tutorial. Ollama local por defecto; demo y OpenAI opcionales.
Las claves solo se leen en servidor, nunca forman parte del State público.
"""
import asyncio
from contextlib import aclosing
import importlib.util
import os
from typing import AsyncIterator
import reflex as rx
from .ollama_chat import PREFERRED_MODELS, OllamaChatError, model_catalog, ollama_chunks

MAX_QUESTION = 2000
MAX_TURNS = 20
MODES = ['Ollama local', 'Demo local', 'OpenAI']


def demo_response(question: str) -> str:
    """Respuesta determinista de práctica, no un modelo de IA ni búsqueda en documentos."""
    text = question.casefold()
    if 'stream' in text or 'yield' in text:
        return ('En esta demostración, streaming significa mostrar la respuesta por fragmentos. '
                'El evento actualiza el último mensaje y usa yield para enviar el cambio al navegador. '
                'asyncio.sleep simula la espera. Con OpenAI los fragmentos llegan del servicio, no de una respuesta predefinida.')
    if 'estado' in text or 'state' in text:
        return ('State guarda la pregunta, el historial y si se está generando una respuesta. '
                'Los controles leen esos valores. Los eventos los modifican y Reflex actualiza la interfaz. '
                'Cada sesión tiene su propio historial; aquí no utilizamos una base de datos.')
    if 'formulario' in text or 'form' in text:
        return ('Un formulario reúne controles y ejecuta on_submit al pulsar Enviar o Enter. '
                'La pregunta usa value y on_change para sincronizarse con State. '
                'Antes de responder comprobamos que no esté vacía y evitamos peticiones simultáneas.')
    if 'reflex' in text:
        return ('Reflex permite construir una interfaz web con componentes Python. '
                'En este chat, qa dibuja los mensajes, chat recorre el historial y action_bar recoge la pregunta. '
                'ChatAppState coordina los eventos y las actualizaciones de la pantalla.')
    return ('Soy una demostración local con respuestas predefinidas, no una IA. '
            'Puedes probar preguntas sobre Reflex, State, formularios o streaming. '
            'Mi objetivo es ayudarte a observar el historial y la respuesta progresiva. '
            'Para respuestas abiertas, configura el modo OpenAI siguiendo la guía del ejercicio.')


def integration_error(mode: str) -> str:
    if mode in ('Demo local', 'Ollama local'):
        return ''
    if not os.environ.get('OPENAI_API_KEY'):
        return 'Falta OPENAI_API_KEY en el servidor. Usa Demo local o configura la integración y reinicia Reflex.'
    if importlib.util.find_spec('openai') is None:
        return 'Falta el paquete openai. Instálalo en el mismo entorno de Reflex o usa Demo local.'
    return ''


async def response_chunks(mode: str, messages: list[dict[str,str]], model: str = '') -> AsyncIterator[str]:
    """Proveedor intercambiable: el resto de la interfaz no depende de su API."""
    if mode == 'Demo local':
        for word in demo_response(messages[-1]['content']).split(' '):
            await asyncio.sleep(.035)
            yield word + ' '
        return
    if mode == 'Ollama local':
        async with aclosing(ollama_chunks(model,messages)) as stream:
            async for text in stream:
                yield text
        return
    from openai import AsyncOpenAI
    # OPENAI_MODEL permite seleccionar un modelo disponible en tu proyecto de API.
    async with AsyncOpenAI(api_key=os.environ['OPENAI_API_KEY'],timeout=30,max_retries=0) as client:
        async with client.responses.stream(
            model=os.environ.get('OPENAI_MODEL','gpt-4o-mini'),
            instructions='Responde en español de forma clara. Eres un asistente didáctico de Python y Reflex.',
            input=messages, max_output_tokens=800, store=False,
        ) as stream:
            async for event in stream:
                if event.type == 'response.output_text.delta':
                    yield event.delta
                elif event.type == 'response.refusal.delta':
                    yield event.delta
                elif event.type in ('error','response.failed'):
                    raise RuntimeError('El proveedor no pudo completar la respuesta.')
            result = await stream.get_final_response()
            if result.status != 'completed':
                raise RuntimeError('El proveedor terminó con una respuesta incompleta.')


class ChatAppState(rx.State):
    question: str = ''
    chat_history: list[tuple[str,str]] = []
    processing: bool = False
    stop_requested: bool = False
    mode: str = 'Ollama local'
    ollama_model: str = 'novelista:latest'
    ollama_models: list[str] = list(PREFERRED_MODELS)
    ollama_excluded: list[str] = []
    ollama_status: str = 'Pulsa Actualizar modelos para comprobar la conexión.'
    ollama_error: str = ''
    loading_models: bool = False
    error: str = ''
    status: str = 'Listo para practicar'

    @rx.var
    def turns(self) -> int:
        return len(self.chat_history)

    @rx.event
    def set_question(self, value: str):
        if not self.processing:
            self.question = value[:MAX_QUESTION]

    @rx.event
    def set_mode(self, value: str):
        if not self.processing and value in MODES and value != self.mode:
            # No mezclar respuestas locales con contexto real del proveedor.
            self.mode = value
            self.chat_history = []
            self.error = ''
            self.status = 'Modo cambiado. Conversación nueva.'

    @rx.event
    def set_ollama_model(self, value: str):
        if not self.processing and not self.loading_models and value in self.ollama_models and value != self.ollama_model:
            self.ollama_model = value
            self.chat_history = []
            self.error = ''
            self.status = 'Modelo cambiado. Conversación nueva.'

    @rx.event(background=True)
    async def refresh_ollama(self):
        async with self:
            if self.processing or self.loading_models:
                return
            self.loading_models = True
            self.ollama_error = ''
        try:
            models, excluded = await model_catalog()
            async with self:
                self.ollama_models = models
                self.ollama_excluded = excluded
                if self.ollama_model not in models:
                    self.ollama_model = models[0] if models else ''
                    self.chat_history = []
                self.ollama_status = f'Ollama conectado · {len(models)} modelos de conversación disponibles.'
                if not models:
                    self.ollama_error = 'No hay modelos instalados con capacidad de conversación.'
        except OllamaChatError as exc:
            async with self:
                self.ollama_error = str(exc)
                self.ollama_status = 'Sin conexión confirmada'
        finally:
            async with self:
                self.loading_models = False

    @rx.event
    def use_example(self, text: str):
        if not self.processing:
            self.question = text

    @rx.event
    def clear_chat(self):
        if not self.processing:
            self.chat_history = []
            self.question = ''
            self.error = ''
            self.status = 'Conversación nueva'

    @rx.event
    def request_stop(self):
        if self.processing:
            self.stop_requested = True
            self.status = 'Deteniendo respuesta…'

    # Las esperas de red están fuera del bloqueo; así Detener puede ejecutarse durante el streaming.
    @rx.event(background=True)
    async def answer(self):
        async with self:
            question = self.question.strip()
            if self.processing or not question:
                return
            if len(question) > MAX_QUESTION:
                self.error = f'Máximo {MAX_QUESTION} caracteres por pregunta.'
                return
            if len(self.chat_history) >= MAX_TURNS:
                self.error = f'Has llegado a {MAX_TURNS} turnos. Inicia una conversación nueva.'
                return
            problem = integration_error(self.mode)
            if problem:
                self.error = problem
                return
            mode = self.mode
            model = self.ollama_model if mode == 'Ollama local' else ''
            if self.loading_models:
                self.error = 'Espera a que termine la consulta de modelos.'
                return
            if mode == 'Ollama local' and not model:
                self.error = 'Selecciona un modelo disponible de Ollama.'
                return
            messages = []
            for old_question, old_answer in self.chat_history:
                messages.extend([{'role':'user','content':old_question}, {'role':'assistant','content':old_answer}])
            messages.append({'role':'user','content':question})
            self.processing = True
            self.stop_requested = False
            self.error = ''
            self.status = 'Generando respuesta…'
            self.question = ''
            self.chat_history.append((question,''))
        yield rx.scroll_to('chat-o05-final',False)
        stopped = False
        try:
            async with aclosing(response_chunks(mode,messages,model)) as chunks:
                async for chunk in chunks:
                    async with self:
                        if self.stop_requested:
                            stopped = True
                            break
                        previous = self.chat_history[-1][1]
                        self.chat_history[-1] = (question,previous+chunk)
                    yield rx.scroll_to('chat-o05-final',False)
            async with self:
                if self.stop_requested:
                    stopped = True
                if not self.chat_history[-1][1].strip():
                    self.chat_history.pop()
                    self.question = question
                    self.status = 'Detenida sin respuesta' if stopped else 'No se recibió texto'
                else:
                    self.status = 'Respuesta detenida · texto parcial' if stopped else 'Respuesta completada'
        except Exception as exc:
            # No mostrar mensajes crudos del proveedor (pueden contener datos internos).
            # Quitar el turno fallido evita usar una respuesta incompleta como contexto.
            async with self:
                self.chat_history.pop()
                self.question = question
                self.error = str(exc) if isinstance(exc,OllamaChatError) else 'No se pudo completar la respuesta. Se ha recuperado la pregunta para reintentar. Revisa conexión, acceso al modelo y configuración del servidor.'
                self.status = 'Error en la respuesta'
        finally:
            async with self:
                self.processing = False
                self.stop_requested = False
            yield rx.scroll_to('chat-o05-final',False)


# Componentes del tutorial: qa (una pareja), chat (historial), action_bar (entrada).
def qa(question, answer):
    return rx.vstack(
        rx.box(rx.text('Tú',size='1',weight='bold',margin_bottom='6px'),
               rx.text(question,white_space='pre-wrap'),align_self='end',max_width='90%',
               background_color='#eef2ff',color='#312e81',padding='16px 20px',border_radius='18px',overflow_wrap='anywhere'),
        rx.box(rx.text('Asistente',size='1',weight='bold',margin_bottom='6px'),
               rx.text(rx.cond(answer!='',answer,'Preparando respuesta…'),white_space='pre-wrap'),
               align_self='start',max_width='90%',background_color='#f8fafc',color='#0f172a',
               padding='16px 20px',border='1px solid #e2e8f0',border_radius='18px',overflow_wrap='anywhere'),
        gap='12px',width='100%',margin_bottom='20px')


def chat():
    return rx.box(
        rx.cond(ChatAppState.turns==0,
            rx.center(rx.vstack(rx.icon('messages-square',size=34,color='#6366f1'),
                rx.heading('¿Qué quieres probar?',size='6'),
                rx.text('Empieza con una pregunta sugerida o escribe la tuya.',color='#475569'),
                *[rx.button(text,variant='soft',on_click=ChatAppState.use_example(text)) for text in
                  ['¿Qué es Reflex?','¿Cómo funciona State?','Explícame streaming y yield']],
                align='center',gap='16px'),min_height='350px'),
            rx.foreach(ChatAppState.chat_history,lambda pair:qa(pair[0],pair[1]))),
        rx.box(id='chat-o05-final'),height='460px',overflow_y='auto',padding='20px',
        border='1px solid #e2e8f0',border_radius='16px',background_color='white',width='100%')


def action_bar():
    return rx.form(rx.flex(
        rx.input(value=ChatAppState.question,on_change=ChatAppState.set_question,
                 name='question',placeholder='Escribe una pregunta…',aria_label='Pregunta',
                 max_length=MAX_QUESTION,required=True,disabled=ChatAppState.processing,
                 size='3',flex='1',min_width='180px'),
        rx.button(rx.icon('send',size=17),'Enviar',type='submit',loading=ChatAppState.processing,
                  disabled=ChatAppState.question.strip()=='',size='3'),
        rx.button('Detener',type='button',variant='soft',color_scheme='gray',on_click=ChatAppState.request_stop,
                  disabled=~ChatAppState.processing),gap='12px',flex_wrap='wrap'),
        on_submit=lambda _:ChatAppState.answer(),reset_on_submit=False,width='100%')


def chat_app_05():
    return rx.box(rx.vstack(
        rx.flex(rx.box(rx.badge('o05 · CHAT APP',color_scheme='indigo'),
                 rx.heading('Conversaciones con Python',size='8',margin_top='12px'),
                 rx.text('Del formulario al historial, una respuesta a la vez.',color='#cbd5e1',margin_top='12px')),
                 rx.link('← Inicio',href='/',color='#c7d2fe'),justify='between',gap='20px',flex_wrap='wrap',
                 padding='30px',background_color='#0f172a',color='white',border_radius='20px',width='100%'),
        rx.box(rx.flex(rx.select(MODES,value=ChatAppState.mode,on_change=ChatAppState.set_mode,
                                 disabled=ChatAppState.processing,aria_label='Modo del asistente'),
                rx.badge(ChatAppState.turns,' / 20 turnos'),
                rx.button('Nueva conversación',variant='soft',on_click=ChatAppState.clear_chat,disabled=ChatAppState.processing),
                gap='12px',align='center',flex_wrap='wrap'),
            rx.cond(ChatAppState.mode=='Ollama local',
                rx.vstack(
                    rx.text('Modelo instalado en tu Ollama',weight='bold',size='2'),
                    rx.flex(rx.select(ChatAppState.ollama_models,value=ChatAppState.ollama_model,
                            on_change=ChatAppState.set_ollama_model,placeholder='Selecciona un modelo',
                            disabled=ChatAppState.processing | ChatAppState.loading_models,aria_label='Modelo de Ollama'),
                            rx.button('Actualizar modelos',on_click=ChatAppState.refresh_ollama,loading=ChatAppState.loading_models,
                                      disabled=ChatAppState.processing,variant='soft'),gap='12px',flex_wrap='wrap'),
                    rx.text(ChatAppState.ollama_status,size='2',role='status'),
                    rx.cond(ChatAppState.ollama_excluded.length()>0,
                        rx.box(rx.text('No aptos para conversación (por ejemplo, embeddings):',size='2'),
                               rx.foreach(ChatAppState.ollama_excluded,lambda name:rx.badge(name,color_scheme='gray',margin_right='8px')))),
                    rx.cond(ChatAppState.ollama_error!='',rx.callout(ChatAppState.ollama_error,color_scheme='red',role='alert')),
                    rx.callout('La conversación se envía a tu servidor Ollama local. Cambiar de modelo inicia una conversación nueva. La primera respuesta puede tardar mientras carga el modelo.'),
                    align='stretch',gap='12px',margin_top='16px'),
            rx.cond(ChatAppState.mode=='Demo local',
                rx.callout('Demostración con respuestas predefinidas. No es una IA, no usa Internet y no necesita una clave.',margin_top='16px'),
                rx.callout('Modo OpenAI: al enviar se transmite la pregunta y el historial de esta conversación a la API. Requiere configuración del servidor y puede generar coste. Cambiar de modo limpia el historial.',margin_top='16px'))),
            margin_bottom='4px',width='100%'),
        chat(),action_bar(),
        rx.flex(rx.text(ChatAppState.status,size='2',color='#475569',role='status'),
                rx.text('Historial por sesión · sin base de datos',size='1',color='#64748b'),justify='between',gap='12px',flex_wrap='wrap'),
        rx.cond(ChatAppState.error!='',rx.callout(ChatAppState.error,color_scheme='red',role='alert')),
        rx.accordion.root(rx.accordion.item(header='Cómo funciona · sigue el código',value='code',content=rx.vstack(
            rx.text('1. question guarda lo que escribes; on_change ejecuta set_question.'),
            rx.text('2. Enviar o Enter activa answer, un evento en segundo plano.'),
            rx.text('3. Se añade (pregunta, respuesta vacía) a chat_history y se limpia el campo.'),
            rx.text('4. response_chunks produce fragmentos; cada yield actualiza el navegador.'),
            rx.text('5. Los bloques async with self protegen el estado; las esperas ocurren fuera del bloqueo.'),
            rx.text('6. qa dibuja cada pareja; rx.foreach recorre el historial. Detener conserva el texto parcial.'),
            rx.text('Archivo: o05_chat_app.py. Ollama usa /api/chat en local; OpenAI usa Responses; la demo permite practicar sin modelo.'),
            rx.link('Tutorial de chat de Reflex ↗',href='https://reflex.dev/docs/getting-started/chatapp-tutorial/',is_external=True),
            align='start',gap='12px')),collapsible=True,width='100%'),
        align='stretch',gap='20px',max_width='1000px',margin='0 auto'),
        padding=['16px','32px'],background_color='#f1f5f9',color='#0f172a',min_height='100vh')
