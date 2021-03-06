# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 21:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_auto_20171106_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detail',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detail',
            name='location_drop_off',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detail',
            name='location_pick_up',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detail',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
