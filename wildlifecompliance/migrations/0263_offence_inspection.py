# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-07-25 06:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0262_auto_20190722_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='offence',
            name='inspection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offence_inspection', to='wildlifecompliance.Inspection'),
        ),
    ]
