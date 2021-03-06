# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-04 09:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import works.models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0018_auto_20181130_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoduck',
            name='lig_file',
            field=models.FileField(upload_to=works.models.dock_upload_to, verbose_name='lig_file'),
        ),
        migrations.AlterField(
            model_name='autoduck',
            name='pdb_file',
            field=models.FileField(upload_to=works.models.dock_upload_to, verbose_name='pdb_file'),
        ),
        migrations.AlterField(
            model_name='autoduck2',
            name='lig_file',
            field=models.FileField(upload_to=works.models.dock2_upload_to, verbose_name='lig_file'),
        ),
        migrations.AlterField(
            model_name='autoduck2',
            name='pdb_file',
            field=models.FileField(upload_to=works.models.dock2_upload_to, verbose_name='pdb_file'),
        ),
        migrations.AlterField(
            model_name='autoduck2',
            name='resi_file',
            field=models.FileField(upload_to=works.models.dock2_upload_to, verbose_name='resi_file'),
        ),
        migrations.AlterField(
            model_name='virtualscreen',
            name='pdb_file',
            field=models.FileField(upload_to=works.models.screen_upload_to, verbose_name='pdb_file'),
        ),
        migrations.AlterField(
            model_name='virtualscreen',
            name='user_db',
            field=models.FileField(null=True, upload_to=works.models.screen_upload_to, verbose_name='user_db'),
        ),
        migrations.AlterField(
            model_name='virtualscreen',
            name='work_decs',
            field=models.CharField(default='', max_length=100, verbose_name='work_decs'),
        ),
        migrations.AlterField(
            model_name='virtualscreen2',
            name='pdb_file',
            field=models.FileField(upload_to=works.models.screen2_upload_to, verbose_name='pdb_file'),
        ),
        migrations.AlterField(
            model_name='virtualscreen2',
            name='resi_file',
            field=models.FileField(upload_to=works.models.screen2_upload_to, verbose_name='resi_file'),
        ),
        migrations.AlterField(
            model_name='virtualscreen2',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='virtualscreen2',
            name='user_db',
            field=models.FileField(null=True, upload_to=works.models.screen2_upload_to, verbose_name='user_db'),
        ),
    ]
