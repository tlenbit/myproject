# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-03 08:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_auto_20171031_1412'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playlist_entry',
            old_name='votes',
            new_name='rating',
        ),
    ]