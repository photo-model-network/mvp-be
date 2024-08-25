# Generated by Django 5.0.7 on 2024-08-23 10:55

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studio',
            options={'verbose_name': '스튜디오', 'verbose_name_plural': '스튜디오'},
        ),
        migrations.AlterField(
            model_name='studio',
            name='id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False),
        ),
    ]
