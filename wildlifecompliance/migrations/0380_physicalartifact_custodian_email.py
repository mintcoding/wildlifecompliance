# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-01-14 23:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0379_compliancemanagementemailuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='physicalartifact',
            name='custodian_email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
