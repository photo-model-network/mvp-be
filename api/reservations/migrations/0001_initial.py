# Generated by Django 5.0.7 on 2024-09-09 04:44

import django.db.models.deletion
import shortuuid.django_fields
import uuid
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
                ('payment_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('payment_amount', models.PositiveIntegerField(default=0)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('payment_status', models.CharField(choices=[('대기중', '대기중'), ('입금완료', '입금완료'), ('배송등록', '배송등록'), ('구매결정', '구매결정'), ('에스크로 릴리스', '에스크로 릴리스'), ('결제완료', '결제완료'), ('에스크로 환불', '에스크로 환불'), ('결제취소', '결제취소')], default='대기중', max_length=20)),
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('대기중', '대기중'), ('예약확정', '예약확정'), ('예약취소', '예약취소'), ('작업중', '작업중'), ('작업완료', '작업완료'), ('구매확정', '구매확정')], default='대기중', max_length=15)),
                ('request', models.TextField(blank=True, null=True)),
                ('package_title', models.CharField(blank=True, max_length=150, null=True)),
                ('additional_people', models.PositiveIntegerField(blank=True, default=0)),
                ('filming_date', models.DateField()),
                ('filming_start_time', models.TimeField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='packages.package')),
            ],
            options={
                'verbose_name': '예약',
                'verbose_name_plural': '예약',
                'ordering': ['-created_at'],
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
                ('duration_time', models.PositiveIntegerField(default=0)),
                ('price', models.PositiveIntegerField(default=0)),
                ('additional_person_price', models.PositiveIntegerField(default=0)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='reservations.reservation')),
            ],
            options={
                'verbose_name': '예약 당시 옵션',
                'verbose_name_plural': '예약 당시 옵션',
                'ordering': ['-created_at'],
            },
        ),
    ]
