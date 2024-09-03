# Generated by Django 5.0.7 on 2024-09-03 11:47

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False),
        ),
    ]