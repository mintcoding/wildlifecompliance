# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-08-13 03:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0280_auto_20190812_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='InspectionTypeApprovalDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('_file', models.FileField(max_length=255, upload_to=b'')),
                ('log_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_document', to='wildlifecompliance.InspectionType')),
            ],
        ),
    ]
