# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-31 19:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightControl', '0005_auto_20161030_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='gpio_pin',
            field=models.IntegerField(default=None),
        ),
    ]