# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worklog', '0003_auto_20190602_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='paid',
        ),
    ]
