# Generated by Django 5.0.7 on 2024-09-09 21:54

import api.chats.models
import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False)),
                ('participants', models.ManyToManyField(related_name='chatrooms', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '채팅방',
                'verbose_name_plural': '채팅방',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=api.chats.models.save_message_file)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chats.chatroom')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '메시지',
                'verbose_name_plural': '메시지',
                'indexes': [models.Index(fields=['room', 'timestamp'], name='chats_messa_room_id_5fcad8_idx')],
            },
        ),
    ]
