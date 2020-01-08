# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_pricelist'),
        ('userprofile', '0004_auto_20190602_2126'),
        ('worklog', '0004_remove_entry_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Valuation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('date', models.DateField()),
                ('expiration_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name=b'klient', to='customers.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='ValuationItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name=b'opis prac / etapu')),
                ('min_hours', models.PositiveIntegerField()),
                ('max_hours', models.PositiveIntegerField()),
                ('notes', models.TextField(blank=True)),
                ('role', models.ForeignKey(to='userprofile.Role', on_delete=models.PROTECT)),
                ('valuation', models.ForeignKey(to='worklog.Valuation', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name': 'wykonana praca', 'verbose_name_plural': 'wykonane prace'},
        ),
    ]
