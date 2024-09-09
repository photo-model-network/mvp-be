# Generated by Django 5.0.7 on 2024-09-09 05:24

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False)),
                ('name', models.CharField(default='익명의 사용자', max_length=100)),
                ('avatar', models.URLField(blank=True, default='https://cdn-icons-png.flaticon.com/512/149/149071.png')),
                ('bio', models.TextField(blank=True, default='안녕하세요, 저의 프로필에 방문해주셔서 감사합니다.')),
                ('type', models.CharField(choices=[('개인', '개인'), ('개인사업자', '개인사업자'), ('법인사업자', '법인사업자')], default=None, max_length=10, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('real_name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('is_identified', models.BooleanField(default=False)),
                ('bank_account', models.CharField(blank=True, max_length=20, null=True)),
                ('bank_code', models.CharField(blank=True, max_length=3, null=True)),
                ('bank_verification_code', models.CharField(blank=True, max_length=4, null=True)),
                ('bank_verified', models.BooleanField(default=False)),
                ('business_license_number', models.CharField(blank=True, max_length=30, null=True)),
                ('is_business', models.BooleanField(default=False)),
                ('has_studio', models.BooleanField(default=False)),
                ('favorite_artists', models.ManyToManyField(blank=True, related_name='favorited_by', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
