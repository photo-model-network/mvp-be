import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message


import logging

User = get_user_model()

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        self.other_user = self.scope["url_route"]["kwargs"]["uid"]

        if not self.user.is_authenticated:
            await self.close()
            return

        try:
            other_user = await self.get_user(self.other_user)
        except User.DoesNotExist:
            await self.close()
            return

        self.room = await self.get_or_create_chatroom(self.user.id, other_user.id)
        self.room_group_name = f"chat_{self.room.id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        file_url = data.get("file_url", "")

        if message:
            await self.save_message(self.user, self.room, message, "")
        elif file_url:
            await self.save_message(self.user, self.room, "", file_url)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "file_url": file_url,
                "sender": self.user.id,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        file_url = event["file_url"]
        sender = event["sender"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "file_url": file_url,
                    "sender": sender,
                }
            )
        )

    @database_sync_to_async
    def get_user(self, uid):
        return User.objects.get(id=uid)

    @database_sync_to_async
    def get_or_create_chatroom(self, uid1, uid2):

        users = User.objects.filter(id__in=[uid1, uid2])
        room = ChatRoom.objects.filter(participants__in=users).distinct()

        if room.count() == 1:
            return room.first()
        elif room.count() > 1:
            # 예외 처리 또는 로깅: 동일한 조건의 방이 여러 개 존재할 때
            raise Exception("해당 참가자들에 대해 여러 개의 채팅방이 발견되었습니다.")
        else:
            # 채팅방을 새로 생성
            room = ChatRoom.objects.create()
            room.participants.add(*users)
            room.save()
            return room

    @database_sync_to_async
    def save_message(self, sender, room, message, file_url):
        return Message.objects.create(sender=sender, room=room, message=message, file=file_url)
