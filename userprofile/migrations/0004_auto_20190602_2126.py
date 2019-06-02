# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20190602_1638'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='associate',
            options={'verbose_name': 'wsp\xf3\u0142pracownik', 'verbose_name_plural': 'wsp\xf3\u0142pracownicy'},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': 'rola', 'verbose_name_plural': 'role'},
        ),
        migrations.AlterField(
            model_name='associate',
            name='default_manhour_cost',
            field=models.PositiveIntegerField(verbose_name='domy\u015blny koszt roboczogodziny'),
        ),
        migrations.AlterField(
            model_name='associate',
            name='name',
            field=models.CharField(max_length=120, verbose_name=b'nazwisko'),
        ),
        migrations.AlterField(
            model_name='associate',
            name='roles',
            field=models.ManyToManyField(to='userprofile.Role', verbose_name=b'role', through='userprofile.AssociateRoleCosts'),
        ),
        migrations.AlterField(
            model_name='associate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'konto', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='associaterolecosts',
            name='associate',
            field=models.ForeignKey(verbose_name='wsp\xf3\u0142pracownik', to='userprofile.Associate'),
        ),
        migrations.AlterField(
            model_name='associaterolecosts',
            name='manhour_cost',
            field=models.PositiveIntegerField(verbose_name=b'koszt roboczogodziny'),
        ),
        migrations.AlterField(
            model_name='associaterolecosts',
            name='role',
            field=models.ForeignKey(verbose_name=b'rola', to='userprofile.Role'),
        ),
        migrations.AlterField(
            model_name='role',
            name='manhour_price',
            field=models.PositiveIntegerField(verbose_name='cena sprzeda\u017cy roboczogodziny'),
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=64, verbose_name=b'nazwa'),
        ),
    ]
