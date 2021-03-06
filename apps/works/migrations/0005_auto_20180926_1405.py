# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-26 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0004_autoduck_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='autoduck',
            old_name='name',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='autoduck',
            name='size_z',
            field=models.FloatField(verbose_name='size_z'),
        ),
        migrations.AlterField(
            model_name='virtualscreen',
            name='size_z',
            field=models.FloatField(verbose_name='size_z'),
        ),
    ]
