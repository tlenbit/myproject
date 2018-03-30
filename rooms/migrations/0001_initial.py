# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-15 09:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(choices=[('U', 'Vote up'), ('D', 'Vote down')], max_length=1)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'activity',
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'artist',
            },
        ),
        migrations.CreateModel(
            name='Playlist_entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'playlist_entry',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('playing_entry', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='rooms.Playlist_entry')),
            ],
            options={
                'db_table': 'room',
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'track',
            },
        ),
        migrations.AddField(
            model_name='room',
            name='playlist_tracks',
            field=models.ManyToManyField(through='rooms.Playlist_entry', to='rooms.Track'),
        ),
        migrations.AddField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playlist_entry',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Room'),
        ),
        migrations.AddField(
            model_name='playlist_entry',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Track'),
        ),
        migrations.AddField(
            model_name='playlist_entry',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artist',
            name='track',
            field=models.ManyToManyField(to='rooms.Track'),
        ),
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together=set([('content_type', 'object_id', 'user')]),
        ),
    ]
