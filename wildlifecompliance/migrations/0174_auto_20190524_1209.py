# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-05-24 04:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0173_remove_applicationselectedactivity_renewal_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationselectedactivity',
            name='activity_status',
            field=models.CharField(choices=[('default', 'Default'), ('current', 'Current'), ('expired', 'Expired'), ('cancelled', 'Cancelled'), ('surrendered', 'Surrendered'), ('suspended', 'Suspended'), ('replaced', 'Replaced')], default='default', max_length=40),
        ),
    ]
