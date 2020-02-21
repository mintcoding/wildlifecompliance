# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-02-05 08:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0415_auto_20200205_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legalcase',
            name='court_proceedings',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='legal_case', to='wildlifecompliance.CourtProceedings'),
        ),
    ]