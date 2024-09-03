# Generated by Django 5.0.7 on 2024-09-02 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_alter_reservation_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='payment_status',
            field=models.CharField(choices=[('대기중', '대기중'), ('입금완료', '입금완료'), ('배송등록', '배송등록'), ('구매결정', '구매결정'), ('에스크로 릴리스', '에스크로 릴리스'), ('결제완료', '결제완료'), ('에스크로 환불', '에스크로 환불'), ('결제취소', '결제취소')], default='대기중', max_length=20),
        ),
    ]