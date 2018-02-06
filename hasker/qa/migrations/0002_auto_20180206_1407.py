# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-06 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='slug',
            field=models.SlugField(default='default-slug', max_length=140, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=120),
        ),
    ]
