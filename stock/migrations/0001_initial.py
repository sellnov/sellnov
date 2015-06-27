# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('desc', models.TextField(null=True, blank=True)),
                ('price_net', models.DecimalField(max_digits=22, decimal_places=2)),
                ('price_gross', models.DecimalField(max_digits=22, decimal_places=2)),
                ('service', models.BooleanField()),
                ('pkwiu', models.CharField(max_length=16, null=True, blank=True)),
                ('owner', models.ForeignKey(to='userprofile.BusinessEntity')),
            ],
            options={
                'verbose_name': 'Towar/us\u0142uga',
                'verbose_name_plural': 'Towary/us\u0142ugi',
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('rate', models.DecimalField(max_digits=3, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Stawka VAT',
                'verbose_name_plural': 'Stawki VAT',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16)),
            ],
            options={
                'verbose_name': 'Jednostka miary',
                'verbose_name_plural': 'Jednostki miary',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='tax',
            field=models.ForeignKey(to='stock.Tax'),
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(to='stock.Unit'),
        ),
    ]
