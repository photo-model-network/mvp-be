# Generated by Django 5.0.7 on 2024-08-18 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_alter_reservation_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationoption',
            name='duration_time',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
