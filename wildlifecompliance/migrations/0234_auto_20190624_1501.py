# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-06-24 07:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0233_auto_20190624_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callemail',
            name='referrer',
            field=models.ManyToManyField(blank=True, to='wildlifecompliance.Referrer'),
        ),
    ]
