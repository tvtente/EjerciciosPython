import json
import unittest
from unittest.mock import patch
import httpx
from Ejercicio991Reflex.ollama_chat import model_catalog,ollama_chunks,OllamaChatError


class OllamaTests(unittest.IsolatedAsyncioTestCase):
    async def test_catalog_checks_capabilities(self):
        def handle(request):
            if request.url.path=='/api/tags':
                return httpx.Response(200,json={'models':[{'name':'novelista:latest','capabilities':['completion']},
                    {'name':'tavata-embeddings:latest','capabilities':['embedding']},{'name':'modelo-antiguo'}]})
            return httpx.Response(200,json={'capabilities':['completion']})
        with patch('Ejercicio991Reflex.ollama_chat.client',lambda:httpx.AsyncClient(base_url='http://local',transport=httpx.MockTransport(handle))):
            models,excluded=await model_catalog()
        self.assertEqual(models,['novelista:latest','modelo-antiguo'])
        self.assertEqual(excluded,['tavata-embeddings:latest'])

    async def test_stream_sends_chosen_model_and_history(self):
        requests=[]
        def handle(request):
            if request.url.path=='/api/show':return httpx.Response(200,json={'capabilities':['completion','thinking']})
            requests.append(json.loads(request.content))
            body='\n'.join(json.dumps(item) for item in [
                {'message':{'thinking':'no mostrar','content':''},'done':False},
                {'message':{'content':'Hola '},'done':False},
                {'message':{'content':'local'},'done':True}])
            return httpx.Response(200,text=body)
        messages=[{'role':'user','content':'hola'}]
        with patch('Ejercicio991Reflex.ollama_chat.client',lambda:httpx.AsyncClient(base_url='http://local',transport=httpx.MockTransport(handle))):
            text=''.join([part async for part in ollama_chunks('novelista-qwen:latest',messages)])
        self.assertEqual(text,'Hola local')
        self.assertEqual(requests[0]['model'],'novelista-qwen:latest')
        self.assertEqual(requests[0]['messages'],messages)
        self.assertFalse(requests[0]['think'])

    async def test_embedding_is_not_sent_to_chat(self):
        paths=[]
        def handle(request):
            paths.append(request.url.path)
            return httpx.Response(200,json={'capabilities':['embedding']})
        with patch('Ejercicio991Reflex.ollama_chat.client',lambda:httpx.AsyncClient(base_url='http://local',transport=httpx.MockTransport(handle))):
            with self.assertRaises(OllamaChatError):
                async for _ in ollama_chunks('embedding',[]):pass
        self.assertEqual(paths,['/api/show'])

    async def test_interrupted_stream_is_error(self):
        def handle(request):
            if request.url.path=='/api/show':return httpx.Response(200,json={'capabilities':['completion']})
            return httpx.Response(200,text=json.dumps({'message':{'content':'parcial'},'done':False}))
        with patch('Ejercicio991Reflex.ollama_chat.client',lambda:httpx.AsyncClient(base_url='http://local',transport=httpx.MockTransport(handle))):
            with self.assertRaises(OllamaChatError):
                async for _ in ollama_chunks('modelo',[]):pass


if __name__=='__main__':unittest.main()
