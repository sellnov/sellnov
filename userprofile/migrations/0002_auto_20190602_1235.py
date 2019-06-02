# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Associate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('default_manhour_cost', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AssociateRoleCosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('manhour_cost', models.PositiveIntegerField()),
                ('associate', models.ForeignKey(to='userprofile.Associate')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('manhour_price', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='associaterolecosts',
            name='role',
            field=models.ForeignKey(to='userprofile.Role'),
        ),
        migrations.AddField(
            model_name='associate',
            name='roles',
            field=models.ManyToManyField(to='userprofile.Role', through='userprofile.AssociateRoleCosts'),
        ),
        migrations.AddField(
            model_name='associate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
