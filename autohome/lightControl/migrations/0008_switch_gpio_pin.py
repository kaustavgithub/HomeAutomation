# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-01 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightControl', '0007_remove_switch_gpio_pin'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='gpio_pin',
            field=models.IntegerField(default=1),
        ),
    ]