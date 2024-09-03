# Generated by Django 5.0.7 on 2024-09-03 11:47

import shortuuid.django_fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0014_alter_reservation_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='payment_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
