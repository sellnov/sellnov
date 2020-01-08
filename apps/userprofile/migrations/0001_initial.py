# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessEntity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('short_name', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=128)),
                ('postal_code', models.CharField(max_length=8)),
                ('city', models.CharField(max_length=64)),
                ('nip', models.CharField(max_length=16)),
                ('regon', models.CharField(max_length=8)),
                ('phone', models.CharField(max_length=64, null=True, blank=True)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('bank_name', models.CharField(max_length=64)),
                ('iban', models.CharField(max_length=32)),
                ('employers', models.ManyToManyField(related_name='works_in', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(
                    to=settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Podmiot gospodarczy',
                'verbose_name_plural': 'Podmioty gospodarcze',
            },
        ),
    ]
