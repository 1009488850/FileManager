# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UpDownFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_file', models.CharField(max_length=255, unique=True)),
                ('upload_date', models.DateTimeField(auto_now=True)),
                ('size', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_user', models.CharField(max_length=255, verbose_name='登录用户')),
                ('pub_date', models.DateTimeField(verbose_name='创建时间')),
                ('last_modify', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('del_fileable', '可以删除文件'), ('download_fileable', '可以下载文件'), ('upload_fileable', '可以上传文件')),
            },
        ),
        migrations.AddField(
            model_name='updownfile',
            name='upload_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sharefile.UserProfile'),
        ),
    ]
