# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-29 09:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lightControl', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rooms',
            name='album_logo',
        ),
    ]
