# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-30 08:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lightControl', '0004_auto_20161030_0812'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rooms',
            new_name='Room',
        ),
        migrations.RenameModel(
            old_name='Switchs',
            new_name='Switch',
        ),
        migrations.RenameField(
            model_name='switch',
            old_name='switch',
            new_name='switch_name',
        ),
    ]
