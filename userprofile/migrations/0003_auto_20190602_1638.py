# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20190602_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessentity',
            name='iban',
            field=models.CharField(max_length=33),
        ),
        migrations.AlterField(
            model_name='businessentity',
            name='owner',
            field=models.OneToOneField(
                related_name='business_entity', to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE),
        ),
    ]
