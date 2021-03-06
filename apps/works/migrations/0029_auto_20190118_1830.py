# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-18 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0028_auto_20181228_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtualscreen',
            name='mol_db',
            field=models.CharField(choices=[('zinc', 'zinc'), ('chembl', 'chembl'), ('wi', 'wi'), ('user_db_file', 'user_db_file')], max_length=20, null=True, verbose_name='mol_db'),
        ),
        migrations.AlterField(
            model_name='virtualscreen2',
            name='mol_db',
            field=models.CharField(choices=[('zinc', 'zinc'), ('chembl', 'chembl'), ('wi', 'wi'), ('user_db_file', 'user_db_file')], default=0, max_length=20, null=True, verbose_name='mol_db'),
        ),
    ]
