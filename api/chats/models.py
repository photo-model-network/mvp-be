from django.db import models
from api.common.models import CommonModel
from api.accounts.models import User


class ChatRoom(CommonModel):
    participants = models.ManyToManyField(User, related_name="chatrooms")

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
