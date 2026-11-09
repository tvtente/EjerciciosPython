"""El proveedor se sustituye: ninguna prueba transmite datos a una API."""
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from Ejercicio991Reflex.o05_chat_app import ChatAppState, demo_response


class Session(SimpleNamespace):
    async def __aenter__(self):return self
    async def __aexit__(self,*args):return False


def session(question='¿Qué es Reflex?',mode='Demo local'):
    return Session(question=question,mode=mode,chat_history=[],processing=False,
                   stop_requested=False,error='',status='',loading_models=False)


async def chunks(mode,messages,model=''):
    yield 'Una '
    yield 'respuesta.'


class ChatTests(unittest.IsolatedAsyncioTestCase):
    async def run_answer(self,s,source=chunks):
        with patch('Ejercicio991Reflex.o05_chat_app.response_chunks',source):
            async for _ in ChatAppState.answer.fn(s):pass

    async def test_stream_history_and_guard(self):
        s=session()
        await self.run_answer(s)
        self.assertEqual(s.chat_history,[('¿Qué es Reflex?','Una respuesta.')])
        self.assertFalse(s.processing)
        self.assertEqual(s.question,'')
        self.assertEqual(s.status,'Respuesta completada')
        s.processing=True;s.question='Otra'
        await self.run_answer(s)
        self.assertEqual(len(s.chat_history),1)

    async def test_failure_restores_question_without_partial_turn(self):
        async def fail(mode,messages,model=''):
            yield 'Texto parcial'
            raise RuntimeError('Información interna no visible')
        s=session()
        await self.run_answer(s,fail)
        self.assertEqual(s.chat_history,[])
        self.assertEqual(s.question,'¿Qué es Reflex?')
        self.assertTrue(s.error)
        self.assertNotIn('Información interna',s.error)
        self.assertFalse(s.processing)

    async def test_stop_closes_generator_and_keeps_partial(self):
        s=session();closed=[]
        async def source(mode,messages,model=''):
            try:
                yield 'Parte '
                s.stop_requested=True
                yield 'no añadida'
            finally:closed.append(True)
        await self.run_answer(s,source)
        self.assertEqual(s.chat_history[0][1],'Parte ')
        self.assertTrue(closed)
        self.assertFalse(s.processing)
        self.assertIn('parcial',s.status)

    async def test_empty_limits_and_missing_key_do_not_append(self):
        for text in ['', '   ', 'x'*2001]:
            s=session(text);await self.run_answer(s)
            self.assertEqual(s.chat_history,[])
        s=session();s.chat_history=[('q','a')]*20
        await self.run_answer(s);self.assertTrue(s.error)
        s=session(mode='OpenAI')
        with patch.dict('os.environ',{'OPENAI_API_KEY':''}):await self.run_answer(s)
        self.assertIn('OPENAI_API_KEY',s.error)
        self.assertEqual(s.chat_history,[])

    async def test_context_includes_previous_turns(self):
        s=session('Nueva');s.chat_history=[('Antes','Respuesta anterior')]
        async def capture(mode,messages,model=''):
            self.assertEqual(messages,[{'role':'user','content':'Antes'},
                {'role':'assistant','content':'Respuesta anterior'},{'role':'user','content':'Nueva'}])
            yield 'Respuesta'
        await self.run_answer(s,capture)
        self.assertEqual(len(s.chat_history),2)

    def test_demo_is_identified(self):
        self.assertIn('demostración',demo_response('hola'))


if __name__=='__main__':unittest.main()
