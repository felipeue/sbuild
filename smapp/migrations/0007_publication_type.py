# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-16 23:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smapp', '0006_auto_20161114_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='type',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]
