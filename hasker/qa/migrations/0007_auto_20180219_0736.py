# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-19 07:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0006_auto_20180210_2138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='has_answer',
        ),
        migrations.AddField(
            model_name='question',
            name='correct_answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='correct_for_question', to='qa.Answer'),
        ),
    ]
