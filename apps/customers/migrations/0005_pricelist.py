# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20190602_1638'),
        ('customers', '0004_auto_20190602_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('manhour_price', models.PositiveIntegerField()),
                ('customer', models.ForeignKey(
                    to='customers.Customer', on_delete=models.CASCADE)),
                ('role', models.ForeignKey(
                    to='userprofile.Role', on_delete=models.PROTECT)),
            ],
        ),
    ]
