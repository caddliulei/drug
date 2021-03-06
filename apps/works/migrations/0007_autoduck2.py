# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-26 14:44
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import works.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('works', '0006_auto_20180926_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoDuck2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='\u7528\u6237\u540d')),
                ('work_name', models.CharField(max_length=20, verbose_name='\u4efb\u52a1\u540d\u79f0')),
                ('work_decs', models.CharField(default='', max_length=100, verbose_name='\u4efb\u52a1\u63cf\u8ff0')),
                ('mol_db', models.CharField(choices=[(1, 'zinc'), (2, 'chembl')], max_length=10, verbose_name='\u6570\u636e\u5e93\u9009\u62e9')),
                ('lig_file', models.FileField(upload_to=works.models.upload_to, verbose_name='\u914d\u4f53\u6587\u4ef6')),
                ('pdb_file', models.FileField(upload_to=works.models.upload_to, verbose_name='pdb\u6587\u4ef6')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u5206\u5b50\u5bf9\u63a52',
                'verbose_name_plural': '\u5206\u5b50\u5bf9\u63a52',
            },
        ),
    ]
