# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-05-30 12:11
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import works.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('works', '0031_dock'),
    ]

    operations = [
        migrations.CreateModel(
            name='VirScreen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_name', models.CharField(max_length=20, unique=True, verbose_name='work_name')),
                ('mol_db', models.CharField(choices=[('zinc', 'zinc'), ('chembl', 'chembl'), ('drugbank', 'drugbank'), ('chinese-medicine', 'chinese-medicine'), ('taosu', 'taosu'), ('bailingwei', 'bailingwei'), ('jianqian', 'jianqian')], max_length=20, null=True, verbose_name='mol_db')),
                ('target', models.CharField(max_length=100, null=True, verbose_name='target')),
                ('smiles', models.CharField(max_length=200, null=True, verbose_name='smiles')),
                ('pdb_file', models.FileField(null=True, upload_to=works.models.screen_upload_to, verbose_name='pdb_file')),
                ('lig_file', models.FileField(null=True, upload_to=works.models.screen_upload_to, verbose_name='lig_file')),
                ('status', models.CharField(default='waiting', max_length=10, verbose_name='status')),
                ('email', models.CharField(default='', max_length=100, verbose_name='email')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='add_time')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': '\u865a\u62df\u7b5b\u9009',
                'verbose_name_plural': '\u865a\u62df\u7b5b\u9009',
            },
        ),
        migrations.AddField(
            model_name='dock',
            name='email',
            field=models.CharField(default='', max_length=100, verbose_name='email'),
        ),
    ]