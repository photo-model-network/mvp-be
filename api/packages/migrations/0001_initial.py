# Generated by Django 5.0.7 on 2024-08-16 07:37

import django.db.models.deletion
import shortuuid.django_fields
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PackagePolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '패키지 정책',
                'verbose_name_plural': '패키지 정책',
            },
        ),
        migrations.CreateModel(
            name='PackageProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('inquiry_email', models.EmailField(max_length=254)),
                ('inquiry_phone_number', models.CharField(max_length=20)),
                ('kakao_id', models.CharField(blank=True, max_length=100, null=True)),
                ('kakao_channel_url', models.URLField(blank=True, null=True)),
                ('homepage_url', models.URLField(blank=True, null=True)),
                ('facebook_url', models.URLField(blank=True, null=True)),
                ('twitter_url', models.URLField(blank=True, null=True)),
                ('instagram_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': '패키지 제공자 정보',
                'verbose_name_plural': '패키지 제공자 정보',
            },
        ),
        migrations.CreateModel(
            name='PackageTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': '패키지 검색용 태그',
                'verbose_name_plural': '패키지 검색용 태그',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=128, prefix='', primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('시즌패키지', '시즌패키지'), ('야외스냅', '야외스냅'), ('웨딩', '웨딩'), ('프로필', '프로필'), ('바디프로필', '바디프로필'), ('반려동물', '반려동물'), ('기본촬영대행', '기본촬영대행')], default='프로필', max_length=20)),
                ('title', models.CharField(max_length=255)),
                ('thumbnail', models.URLField()),
                ('location', models.CharField(choices=[('경기', '경기'), ('부산', '부산'), ('서울', '서울'), ('인천', '인천'), ('대구', '대구'), ('광주', '광주'), ('대전', '대전'), ('울산', '울산'), ('세종', '세종'), ('강원', '강원'), ('충북', '충북'), ('충남', '충남'), ('전북', '전북'), ('전남', '전남'), ('경북', '경북'), ('경남', '경남'), ('제주', '제주')], default='서울', max_length=5)),
                ('summary', models.TextField()),
                ('html_content', models.TextField()),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.packagepolicy')),
                ('provider_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.packageprovider')),
            ],
            options={
                'verbose_name': '패키지',
                'verbose_name_plural': '패키지',
            },
        ),
        migrations.CreateModel(
            name='PackageOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField(default=0)),
                ('is_delivered', models.BooleanField(default=False)),
                ('delivery_fee', models.PositiveIntegerField(default=0)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.package')),
            ],
            options={
                'verbose_name': '패키지 옵션',
                'verbose_name_plural': '패키지 옵션',
            },
        ),
        migrations.CreateModel(
            name='PackagePicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.URLField()),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.package')),
            ],
            options={
                'verbose_name': '패키지 소개 이미지',
                'verbose_name_plural': '패키지 소개 이미지',
            },
        ),
        migrations.CreateModel(
            name='PackageReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.package')),
            ],
            options={
                'verbose_name': '패키지 리뷰',
                'verbose_name_plural': '패키지 리뷰',
            },
        ),
        migrations.CreateModel(
            name='PackageTaggedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=22, max_length=22, prefix='')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_tagged_items', to='contenttypes.contenttype', verbose_name='content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='packages.packagetag')),
            ],
            options={
                'verbose_name': '패키지 + 태그',
                'verbose_name_plural': '패키지 + 태그',
            },
        ),
        migrations.AddField(
            model_name='package',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='packages.PackageTaggedItem', to='packages.PackageTag', verbose_name='Tags'),
        ),
    ]
