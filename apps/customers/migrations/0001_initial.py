# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=128)),
                ('postal_code', models.CharField(max_length=8)),
                ('city', models.CharField(max_length=64)),
                ('nip', models.CharField(max_length=16)),
                ('regon', models.CharField(default=b'', max_length=8, blank=True)),
                ('phone', models.CharField(max_length=64, null=True, blank=True)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('www', models.URLField(max_length=255, null=True, blank=True)),
                ('custtype', models.IntegerField(choices=[(0, b'Dostawca/Odbiorca'), (1, b'Dostawca'), (2, b'Odbiorca')])),
                ('owner', models.ForeignKey(
                    to='userprofile.BusinessEntity',
                    on_delete=models.PROTECT)),
            ],
            options={
                'verbose_name': 'Klient',
                'verbose_name_plural': 'Klienci',
            },
        ),
    ]
