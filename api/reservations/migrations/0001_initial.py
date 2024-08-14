# Generated by Django 5.0.7 on 2024-08-14 07:03

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('packages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=128, prefix='', primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('대기중', '대기중'), ('예약확정', '예약확정'), ('예약취소', '예약취소'), ('작업중', '작업중'), ('작업완료', '작업완료'), ('구매확정', '구매확정')], default='대기중', max_length=15)),
                ('package_name', models.CharField(default='', max_length=150)),
                ('package_price', models.PositiveIntegerField(default=0)),
                ('reservation_date', models.DateField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='packages.package')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReservationOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField(default=0)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='reservations.reservation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReservationTimeSlot',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=128, prefix='', primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.reservation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
