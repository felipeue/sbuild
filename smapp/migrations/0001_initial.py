# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-04 16:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('floor', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smapp.Apartment')),
            ],
        ),
        migrations.CreateModel(
            name='UserSM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=20)),
                ('user_type', models.CharField(choices=[('O', 'Owner'), ('C', 'Concierge'), ('R', 'Resident')], max_length=1)),
                ('userOrigin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('rut', models.CharField(max_length=10)),
                ('date', models.DateTimeField()),
                ('note', models.TextField(max_length=200)),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smapp.UserSM')),
            ],
        ),
        migrations.AddField(
            model_name='resident',
            name='residentOrigin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smapp.UserSM'),
        ),
        migrations.AddField(
            model_name='building',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smapp.UserSM'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smapp.Building'),
        ),
    ]