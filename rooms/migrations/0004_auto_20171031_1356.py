# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 13:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_auto_20171031_0942'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Playlist_track',
            new_name='Playlist_entry',
        ),
        migrations.RenameField(
            model_name='track',
            old_name='genre',
            new_name='genres',
        ),
    ]