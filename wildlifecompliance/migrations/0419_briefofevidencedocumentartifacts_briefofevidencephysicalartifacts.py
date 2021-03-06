# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-02-10 02:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0418_auto_20200206_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='BriefOfEvidenceDocumentArtifacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticked', models.BooleanField(default=False)),
                ('document_artifact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_artifacts_boe', to='wildlifecompliance.DocumentArtifact')),
                ('legal_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='legal_case_boe_document_artifacts', to='wildlifecompliance.LegalCase')),
            ],
        ),
        migrations.CreateModel(
            name='BriefOfEvidencePhysicalArtifacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticked', models.BooleanField(default=False)),
                ('legal_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='legal_case_boe_physical_artifacts', to='wildlifecompliance.LegalCase')),
                ('physical_artifact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='physical_artifacts_boe', to='wildlifecompliance.PhysicalArtifact')),
            ],
        ),
    ]
