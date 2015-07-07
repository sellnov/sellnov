# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
        ('userprofile', '0001_initial'),
        ('payments', '0001_initial'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operation_date', models.DateField(verbose_name='Data czynno\u015bci')),
                ('issue_date', models.DateField(verbose_name='Data wystawienia')),
                ('pay_date', models.DateField(verbose_name='Termin p\u0142atno\u015bci')),
                ('location', models.CharField(max_length=128, verbose_name='Miejsce wystawienia')),
                ('number', models.PositiveIntegerField(verbose_name=b'Numer')),
                ('number_fmt', models.CharField(max_length=32, verbose_name='Numer wy\u015bwietlany')),
                ('payment_name', models.CharField(max_length=128, verbose_name='Nazwa p\u0142atno\u015bci')),
                ('comment', models.TextField(null=True, verbose_name=b'Komentarz', blank=True)),
                ('issuer_name', models.CharField(default=b'', max_length=128, verbose_name='Osoba wystawiaj\u0105ca', blank=True)),
                ('paid', models.BooleanField(default=False, verbose_name='Zap\u0142acona')),
                ('doctype', models.CharField(max_length=32, editable=False)),
                ('customer', models.ForeignKey(verbose_name=b'Klient', to='customers.Customer')),
                ('owner', models.ForeignKey(verbose_name=b'Podmiot', to='userprofile.BusinessEntity')),
                ('payment_type', models.ForeignKey(verbose_name='Spos\xf3b p\u0142atno\u015bci', to='payments.PaymentType')),
            ],
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=128)),
                ('unit_name', models.CharField(max_length=32)),
                ('price_net', models.DecimalField(max_digits=22, decimal_places=2)),
                ('price_gross', models.DecimalField(max_digits=22, decimal_places=2)),
                ('quantity', models.DecimalField(max_digits=10, decimal_places=3)),
                ('tax_rate', models.DecimalField(max_digits=3, decimal_places=2)),
                ('tax_value', models.DecimalField(max_digits=22, decimal_places=2)),
                ('total_net', models.DecimalField(max_digits=22, decimal_places=2)),
                ('total_gross', models.DecimalField(max_digits=22, decimal_places=2)),
                ('pkwiu', models.CharField(max_length=16, null=True, blank=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('document', models.ForeignKey(to='documents.Document')),
                ('product', models.ForeignKey(blank=True, to='stock.Product', null=True)),
                ('tax', models.ForeignKey(blank=True, to='stock.Tax', null=True)),
                ('unit', models.ForeignKey(blank=True, to='stock.Unit', null=True)),
            ],
        ),
    ]
