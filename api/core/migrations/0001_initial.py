# Generated by Django 5.0.7 on 2024-09-09 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interaction_type', models.CharField(max_length=50)),
                ('interaction_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '인터랙션',
                'verbose_name_plural': '인터랙션',
            },
        ),
    ]
