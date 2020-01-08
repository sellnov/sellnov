# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_customer_default_manhour_cost'),
        ('userprofile', '0002_auto_20190602_1235'),
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('time', models.DecimalField(max_digits=6, decimal_places=1)),
                ('unit', models.CharField(default=b'h', max_length=3, choices=[(b'm', b'minut'), (b'h', b'godzin'), (b'd', b'dni')])),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('work_finished_at', models.DateField()),
                ('work_started_at', models.DateField(null=True, blank=True)),
                ('paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('associate_role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='userprofile.AssociateRoleCosts', null=True)),
                ('customer', models.ForeignKey(to='customers.Customer', on_delete=django.db.models.deletion.PROTECT)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='tickets.Ticket', null=True)),
            ],
        ),
    ]
