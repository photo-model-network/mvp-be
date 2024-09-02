# Generated by Django 5.0.7 on 2024-08-27 16:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='payment_id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=128, unique=True),
        ),
    ]
