# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-22 00:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smapp', '0011_auto_20161119_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='resident',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='smapp.Resident'),
            preserve_default=False,
        ),
    ]