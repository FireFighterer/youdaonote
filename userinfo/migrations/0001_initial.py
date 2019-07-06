# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-07-04 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=50, verbose_name='密码')),
                ('reg_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='注册时间')),
            ],
        ),
    ]
