# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-05-09 03:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0191_merge_20190509_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='postcode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]