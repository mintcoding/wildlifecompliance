# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-08-17 05:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0500_auto_20200817_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationselectedactivitypurpose',
            name='adjusted_licence_fee',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=8),
        ),
    ]
