# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 18:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_payment_charge_desription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='paid',
        ),
    ]
