# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-07-05 06:46
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0238_sanctionoutcomedocument'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='offender',
            managers=[
                ('active_offenders', django.db.models.manager.Manager()),
            ],
        ),
    ]