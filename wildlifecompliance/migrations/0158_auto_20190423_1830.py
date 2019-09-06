# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-04-23 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0157_merge_20190415_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='application_type',
            field=models.CharField(choices=[('new_licence', 'New'), ('amendment', 'Amendment'), ('renewal', 'Renewal')], default='new_licence', max_length=40, verbose_name='Application Type'),
        ),
    ]