import uuid
import os
from django.db import models
from asgiref.sync import async_to_sync
from shortuuid.django_fields import ShortUUIDField
from channels.layers import get_channel_layer
from api.common.models import CommonModel
from api.accounts.models import User


def save_message_file(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(f"chats/{instance.room.id}", new_filename)


class ChatRoom(CommonModel):
    id = ShortUUIDField(primary_key=True, editable=False)
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
    message = models.TextField(blank=True)
    file = models.FileField(upload_to=save_message_file, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

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
                "file_url": self.file.url if self.file else "",
            },
        )
