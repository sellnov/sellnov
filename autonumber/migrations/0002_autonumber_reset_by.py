# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autonumber', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='autonumber',
            name='reset_by',
            field=models.CharField(default=b'year', max_length=16, choices=[(b'month', 'co miesi\u0105c'), (b'year', 'co rok')]),
        ),
    ]
