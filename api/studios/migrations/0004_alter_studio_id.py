# Generated by Django 5.0.7 on 2024-09-03 04:10

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0003_alter_studio_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studio',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=22, primary_key=True, serialize=False),
        ),
    ]