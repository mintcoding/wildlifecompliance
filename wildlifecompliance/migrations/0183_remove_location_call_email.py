# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-05-05 23:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0182_auto_20190505_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='call_email',
        ),
    ]
