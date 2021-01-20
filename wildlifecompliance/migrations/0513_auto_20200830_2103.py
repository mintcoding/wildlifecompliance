# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-08-30 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0512_applicationselectedactivitypurpose_purpose_species_json'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='returntype',
            name='species_required',
        ),
        migrations.AddField(
            model_name='returntype',
            name='species_list',
            field=models.CharField(choices=[('regulated', 'Regulated Species List'), ('application', 'Application Species List'), ('none', 'No Species List')], default='none', max_length=30, verbose_name='Species List'),
        ),
    ]