# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-02-11 07:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0421_auto_20200211_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='briefofevidencephysicalartifacts',
            name='details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='prosecutionbriefphysicalartifacts',
            name='details',
            field=models.TextField(blank=True, null=True),
        ),
    ]
