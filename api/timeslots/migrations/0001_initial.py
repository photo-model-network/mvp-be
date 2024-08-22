# Generated by Django 5.0.7 on 2024-08-21 15:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnavailableTimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unavaliable_timeslots', to='packages.package')),
            ],
            options={
                'verbose_name': '예약 불가 날짜/시간 설정',
                'verbose_name_plural': '예약 불가 날짜/시간 설정',
                'unique_together': {('package', 'start_datetime', 'end_datetime')},
            },
        ),
    ]
