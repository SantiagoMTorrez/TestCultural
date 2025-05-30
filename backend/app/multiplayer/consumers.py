# multiplayer/consumers.py

import json
import asyncio
import logging
from datetime import timedelta
from urllib.parse import parse_qs

from django.utils import timezone
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps
from typing import Dict, TypeVar
logger = logging.getLogger(__name__)

GS = TypeVar('GS', bound="GameSession") 

class GameSession:
    """
    Gestor singleton de sesiones de juego en memoria.
    Mantiene por test_id:
      - instancia de Test
      - lista de TestQuestion
      - índice de pregunta actual
      - timestamp de fin de pregunta
      - estado de ejecución
      - host_id (usuario que inició la sesión)
    """
    _sessions = {}

    @classmethod
    def get(cls, test_id) -> GS:
        if test_id not in cls._sessions:
            cls._sessions[test_id] = cls(test_id)
        return cls._sessions[test_id]

    def __init__(self, test_id):
        self.test_id = test_id
        self.test = None
        self.questions = []
        self.current_index = 0
        self.is_running = False
        self.has_ended = False
        self.end_time = None
        self.host_id = None
        self.counter = 3

    async def _load_test(self):
        if self.test is None:
            Test = apps.get_model('trivia', 'Test')
            self.test = await sync_to_async(Test.objects.get)(id=self.test_id)

    async def _load_questions(self):
        await self._load_test()
        TestQuestion = apps.get_model('trivia', 'TestQuestion')
        qs = await sync_to_async(list)(
            TestQuestion.objects
                .filter(test_id=self.test_id)
                .select_related('question')
                .order_by('question_number')
        )
        self.questions = qs

    async def start(self, group_name, channel_layer):
        if self.is_running:
            return
        await self._load_questions()
        self.is_running = True
        await self._send_current_question(group_name, channel_layer)
        self.test.started_at = timezone.now()
        await sync_to_async(self.test.save)()

    async def _send_current_question(self, group_name, channel_layer):
        tq = self.questions[self.current_index]
        question = tq.question
        opts = [
            {"id": opt.id, "text": opt.text, "correct": opt.correct, "points": question.score}
            for opt in await sync_to_async(list)(question.answer_options.all())
        ]
        now = timezone.now()
        limit_secs = self.test.time_limit_minutes/len(self.questions) * 60
        self.end_time = now + timedelta(seconds=limit_secs)
        payload = {
            "action":   "question",
            "index":    self.current_index,
            "question": {"text": question.text, "options": opts},
            "start_ts": now.timestamp(),
            "end_ts":   self.end_time.timestamp(),
        }
        await channel_layer.group_send(
            group_name,
            {"type": "game.event", "payload": payload}
        )
        asyncio.create_task(
            self._schedule_advance(group_name, channel_layer, limit_secs)
        )

    async def _run_count_down(self, group_name, channel_layer):
        if(self.counter <= 0):
            await self.advance(group_name, channel_layer)
        else:
            await asyncio.sleep(1)
            payload = {
                "action":   "counter",
                "index":    self.counter,
            }
            await channel_layer.group_send(group_name, {"type": "game.event", "payload":payload})
            self.counter -= 1
            asyncio.create_task(self._run_count_down(group_name, channel_layer))

    async def _schedule_advance(self, group_name, channel_layer, delay):
        if(self.current_index+1 < len(self.questions)):
            self.counter = 3
        else:
            self.counter = 0
        await asyncio.sleep(delay)
        await self._run_count_down(group_name, channel_layer)

    async def advance(self, group_name, channel_layer):
        self.current_index += 1
        if self.current_index < len(self.questions):
            await self._send_current_question(group_name, channel_layer)
        else:
            await channel_layer.group_send(
                group_name,
                {"type": "game.event", "payload": {"action": "game_over"}}
            )
            self.test.ended = True
            await sync_to_async(self.test.save)()

class GameConsumer(AsyncWebsocketConsumer):
    """
    WS consumer que autentica por token y administra la partida.
    """
    async def connect(self):
        # Extraer token de la query string
        query_string = self.scope.get('query_string', b'').decode()
        params = parse_qs(query_string)
        token_key = params.get('token', [None])[0]
        if not token_key:
            await self.close(code=4001)
            return
        # Validar token y cargar usuario con select_related
        TokenModel = apps.get_model('authtoken', 'Token')
        try:
            token = await sync_to_async(
                lambda: TokenModel.objects.select_related('user').get(key=token_key)
            )()
            user = token.user  # ya pre-cargado
            self.scope['user'] = user
        except TokenModel.DoesNotExist:
            await self.close(code=4002)
            return
        # Identificar partida y grupo
        self.test_id = int(self.scope['url_route']['kwargs']['test_id'])
        self.group_name = f"game_{self.test_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        # Inicializar sesión y participación en BD
        self.session = GameSession.get(self.test_id)
        if self.session.is_running or self.session.has_ended:
            self.channel_layer.group_discard(self.group_name, self.channel_name)
            return 
        TestParticipation = apps.get_model('trivia', 'TestParticipation')
        self.participation, _ = await sync_to_async(
            TestParticipation.objects.get_or_create
        )(user=self.scope['user'], test_id=self.test_id)
        # Asignar host si es primer usuario
        if self.session.host_id is None:
            self.session.host_id = self.scope['user'].id
        # Broadcast lista de jugadores
        await self.broadcast_players()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get('action')
            handler = getattr(self, f"action_{action}", None)
            if callable(handler):
                await handler(data)
            else:
                logger.warning(f"Acción desconocida: {action}")
        except json.JSONDecodeError:
            logger.error("Payload no es JSON válido.")

    async def action_start(self, data):
        await self.session.start(self.group_name, self.channel_layer)

    async def action_submit(self, data):
        answer_id = data.get('answer_id')
        pr = await sync_to_async(self._record_response)(answer_id)
        payload = {'action': 'update_score', 'user_id': self.scope['user'].id, 'score': pr.score}
        await self.channel_layer.group_send(self.group_name, {'type': 'game.event', 'payload': payload})
        await self.broadcast_players()

    async def action_time_sync(self, data):
        ts = timezone.now().timestamp()
        await self.send(text_data=json.dumps({'action': 'time_sync', 'server_ts': ts}))

    async def broadcast_players(self):
        TestParticipation = apps.get_model('trivia', 'TestParticipation')
        participations = await sync_to_async(list)(
            TestParticipation.objects.select_related('user').filter(test_id=self.test_id).order_by("-score")
        )
        players = [{'id': p.user.id, 'username': p.user.name, 'score': p.score} for p in participations]
        payload = {'action': 'players_list', 'players': players, 'host_id': self.session.host_id}
        await self.channel_layer.group_send(self.group_name, {'type': 'game.event', 'payload': payload})

    def _record_response(self, answer_id):
        AnswerOption = apps.get_model('trivia', 'AnswerOption')
        ParticipationResponse = apps.get_model('trivia', 'ParticipationResponse')
        tq = self.session.questions[self.session.current_index]
        pr = ParticipationResponse.objects.create(
            test_participation=self.participation,
            test_question=tq,
            answer_option_id=answer_id,
            accessed_at=timezone.now(),
            responded_at=timezone.now(),
        )
        correct = AnswerOption.objects.get(id=answer_id).correct
        pr.score = tq.question.score if correct else 0.0
        pr.save()
        self.participation.score += pr.score
        self.participation.save(update_fields=['score'])
        return pr.score

    async def game_event(self, event):
        await self.send(text_data=json.dumps(event['payload']))
