# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='lyrics',
            field=models.CharField(default='', max_length=16384),
        ),
    ]