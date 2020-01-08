# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyTransferBalance',
            fields=[
                ('year', models.PositiveIntegerField(primary_key=True)),
                ('month', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('sum_amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('balance', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
            options={
                'db_table': 'cash_transfer_monthly_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TransferWithBalance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('balance', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
            options={
                'db_table': 'cash_transfer_with_balance_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=64)),
                ('estimated_amount', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('draft', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('date', '-created'),
            },
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('account', models.ForeignKey(to='cash.Account', on_delete=models.DO_NOTHING)),
                ('operation', models.ForeignKey(to='cash.Operation', on_delete=models.DO_NOTHING)),
            ],
        ),
    ]
