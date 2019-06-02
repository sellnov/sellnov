# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0003_customer_default_manhour_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(null=True, blank=True)),
                ('estimated_price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('accepted_price', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('acceptance', models.CharField(blank=True, max_length=16, null=True, db_index=True, choices=[(b'accepted', b'zaakceptowana'), (b'rejected', b'odrzucona')])),
                ('accepted_at', models.DateTimeField(null=True, blank=True)),
                ('accepted_by', models.ForeignKey(related_name='accepted_pricings', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(db_index=True, max_length=16, choices=[(b'order', b'zapotrzebowanie'), (b'warranty', b'reklamacja'), (b'issue', b'problem')])),
                ('status', models.CharField(default=b'new', max_length=16, db_index=True, choices=[(b'new', b'nowe'), (b'pricing', b'wycena'), (b'queued', b'przyj\xc4\x99te do realizacji'), (b'inprogress', b'w toku'), (b'rejected', b'oferta odrzucona'), (b'closed', b'zamkni\xc4\x99te')])),
                ('resolution', models.CharField(default=b'unresolved', max_length=16, db_index=True, choices=[(b'unresolved', b'nierozwi\xc4\x85zane'), (b'cancelled', b'anulowane'), (b'done', b'zako\xc5\x84czone'), (b'overpriced', b'zbyt wysoki koszt'), (b'nobudget', b'brak \xc5\x9brodk\xc3\xb3w na realizacj\xc4\x99')])),
                ('issuer_email', models.EmailField(max_length=255, null=True, blank=True)),
                ('issuer_name', models.CharField(max_length=255, null=True, blank=True)),
                ('title', models.CharField(max_length=120, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('issued_at', models.DateField()),
                ('due_date', models.DateField(null=True, blank=True)),
                ('total_price', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price_accepted_at', models.DateTimeField(null=True, blank=True)),
                ('work_accepted_at', models.DateTimeField(null=True, blank=True)),
                ('started_at', models.DateTimeField(null=True, blank=True)),
                ('finished_at', models.DateTimeField(null=True, blank=True)),
                ('closed_at', models.DateTimeField(null=True, blank=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='customers.Customer', null=True)),
                ('issuer', models.ForeignKey(related_name='issued_tickets', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('price_accepted_by', models.ForeignKey(related_name='price_accepted_tickets', on_delete=django.db.models.deletion.PROTECT, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('work_accepted_by', models.ForeignKey(related_name='work_accepted_tickets', on_delete=django.db.models.deletion.PROTECT, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='pricing',
            name='ticket',
            field=models.ForeignKey(to='tickets.Ticket'),
        ),
    ]
