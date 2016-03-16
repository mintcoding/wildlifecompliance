# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-16 08:01
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ledger.accounts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=128)),
                ('last_name', models.CharField(blank=True, max_length=128)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into the admin site.')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting ledger.accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(choices=[('Mr', 'Mr'), ('Miss', 'Miss'), ('Mrs', 'Mrs'), ('Ms', 'Ms'), ('Dr', 'Dr')], default='Mr', max_length=100, null=True, verbose_name='title')),
                ('dob', models.DateField(null=True, verbose_name='date of birth')),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='phone number')),
                ('mobile_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='mobile number')),
                ('fax_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='fax number')),
                ('organisation', models.CharField(blank=True, help_text='organisation, institution or company', max_length=300, null=True, verbose_name='organisation')),
                ('extra_data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', ledger.accounts.models.EmailUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, choices=[('Mr', 'Mr'), ('Miss', 'Miss'), ('Mrs', 'Mrs'), ('Ms', 'Ms'), ('Dr', 'Dr')], max_length=64)),
                ('first_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('line1', models.CharField(max_length=255)),
                ('line2', models.CharField(blank=True, max_length=255)),
                ('line3', models.CharField(blank=True, max_length=255)),
                ('locality', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, choices=[('ACT', 'ACT'), ('NSW', 'NSW'), ('NT', 'NT'), ('QLD', 'QLD'), ('SA', 'SA'), ('TAS', 'TAS'), ('VIC', 'VIC'), ('WA', 'WA')], max_length=255)),
                ('postcode', models.IntegerField(blank=True, null=True)),
                ('search_text', models.TextField(editable=False)),
            ],
            options={
                'verbose_name_plural': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('file', models.FileField(upload_to='%Y/%m/%d')),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='emailuser',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts.Address'),
        ),
        migrations.AddField(
            model_name='emailuser',
            name='documents',
            field=models.ManyToManyField(to='accounts.Document'),
        ),
        migrations.AddField(
            model_name='emailuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='emailuser',
            name='postal_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts.Address'),
        ),
        migrations.AddField(
            model_name='emailuser',
            name='residential_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts.Address'),
        ),
        migrations.AddField(
            model_name='emailuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
