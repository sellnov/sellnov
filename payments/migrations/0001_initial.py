# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('transfer', models.BooleanField()),
                ('due_days', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Spos\xf3b p\u0142atno\u015bci',
                'verbose_name_plural': 'Sposoby p\u0142atno\u015bci',
            },
        ),
    ]
