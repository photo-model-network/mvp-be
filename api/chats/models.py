import shortuuid
from django.db import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from api.common.models import CommonModel
from api.accounts.models import User


class ChatRoom(CommonModel):
    id = models.CharField(
        max_length=22, default=shortuuid.uuid, primary_key=True, editable=False
    )
    participants = models.ManyToManyField(User, related_name="chatrooms")

    def __str__(self):
        participants_list = ", ".join(
            [str(participant) for participant in self.participants.all()]
        )
        return f"{participants_list}"

    class Meta:
        verbose_name = "채팅방"
        verbose_name_plural = "채팅방"


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "메시지"
        verbose_name_plural = "메시지"
        indexes = [
            models.Index(fields=["room", "timestamp"]),
        ]

    def send_message(self):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{self.room.id}",
            {
                "type": "chat_message",
                "sender": self.sender.id,
                "message": self.message,
            },
        )
