"""Adaptador local de Ollama: catálogo, capacidades y streaming NDJSON.

La petición sale del backend Reflex, no del navegador: no requiere cambiar CORS.
"""
import json
import os
from typing import AsyncIterator
import httpx

PREFERRED_MODELS = ['novelista:latest', 'novelista-qwen:latest', 'directorporno:latest', 'tavata-fanvue:latest']


class OllamaChatError(RuntimeError):
    """Error de conexión o modelo que se puede presentar en la interfaz."""


def ollama_url() -> str:
    url = os.environ.get('OLLAMA_HOST','http://127.0.0.1:11434').strip().rstrip('/')
    return url if '://' in url else 'http://' + url


def client():
    # La primera carga de un modelo puede ser lenta. No usar proxies para localhost.
    return httpx.AsyncClient(base_url=ollama_url(),trust_env=False,
                             timeout=httpx.Timeout(180,connect=5))


async def model_catalog() -> tuple[list[str], list[str]]:
    """Consultar capacidades; no asumir que un nombre de modelo implica chat."""
    try:
        async with client() as http:
            response = await http.get('/api/tags',timeout=10)
            response.raise_for_status()
            models = response.json().get('models',[])
            available, excluded = [], []
            for item in models:
                name = item.get('name') or item.get('model')
                if not isinstance(name,str):
                    continue
                capabilities = item.get('capabilities')
                if capabilities is None:
                    details = await http.post('/api/show',json={'model':name},timeout=10)
                    details.raise_for_status()
                    capabilities = details.json().get('capabilities',[])
                (available if 'completion' in capabilities else excluded).append(name)
            available.sort(key=lambda name:(PREFERRED_MODELS.index(name) if name in PREFERRED_MODELS else len(PREFERRED_MODELS),name))
            return available,sorted(excluded)
    except (httpx.HTTPError,ValueError,TypeError) as exc:
        raise OllamaChatError('No se pudo consultar Ollama. Comprueba que está en marcha en el puerto 11434 y pulsa Actualizar modelos.') from exc


async def ollama_chunks(model: str, messages: list[dict[str,str]]) -> AsyncIterator[str]:
    """Leer cada JSON por línea. Ignorar el campo thinking y emitir solo content."""
    if not model:
        raise OllamaChatError('Selecciona un modelo de Ollama para conversar.')
    try:
        async with client() as http:
            check = await http.post('/api/show',json={'model':model},timeout=10)
            if check.status_code == 404:
                raise OllamaChatError('El modelo seleccionado ya no está instalado. Actualiza la lista.')
            check.raise_for_status()
            capabilities = check.json().get('capabilities',[])
            if capabilities and 'completion' not in capabilities:
                raise OllamaChatError('Este modelo solo genera embeddings y no puede responder en el chat.')
            request = {'model':model,'messages':messages,'stream':True,
                       'options':{'num_predict':800},'keep_alive':'5m'}
            # Modelos con razonamiento: pedir respuesta directa si soportan desactivarlo.
            if 'thinking' in capabilities:
                request['think'] = False
            async with http.stream('POST','/api/chat',json=request) as response:
                if response.status_code == 404:
                    raise OllamaChatError('Ollama no encuentra ese modelo. Actualiza la lista.')
                if response.status_code >= 400:
                    raise OllamaChatError(f'Ollama rechazó la petición (HTTP {response.status_code}). Revisa el modelo y la memoria disponible.')
                completed = False
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    chunk = json.loads(line)
                    if chunk.get('error'):
                        raise OllamaChatError('Ollama no pudo generar la respuesta. Revisa su registro y la memoria disponible.')
                    text = chunk.get('message',{}).get('content','')
                    if isinstance(text,str) and text:
                        yield text
                    if chunk.get('done'):
                        completed = True
                        break
                if not completed:
                    raise OllamaChatError('La conexión con Ollama se interrumpió antes de finalizar. Puedes reintentar.')
    except OllamaChatError:
        raise
    except httpx.ConnectError as exc:
        raise OllamaChatError('No se puede conectar con Ollama en local. Comprueba el servicio y OLLAMA_HOST.') from exc
    except httpx.TimeoutException as exc:
        raise OllamaChatError('Ollama tardó demasiado en responder. Prueba un modelo más pequeño o revisa la memoria disponible.') from exc
    except (httpx.HTTPError,ValueError,TypeError) as exc:
        raise OllamaChatError('No se pudo leer la respuesta de Ollama. Comprueba el servicio y reintenta.') from exc
