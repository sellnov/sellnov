# encoding: utf-8

import six

from django.conf import settings
from django.db import models


class UnitManager(models.Manager):
    def get_default(self):
        return self.get_queryset().get(name=settings.DEFAULT_PRODUCT_UNIT)


class Unit(models.Model):
    name = models.CharField(max_length=16)
    objects = UnitManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Jednostka miary'
        verbose_name_plural = 'Jednostki miary'


class TaxManager(models.Manager):
    def get_default(self):
        return self.get_queryset().get(rate=settings.DEFAULT_TAX_RATE)


class Tax(models.Model):
    name = models.CharField(max_length=32)
    rate = models.DecimalField(max_digits=3, decimal_places=2)
    objects = TaxManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Stawka VAT'
        verbose_name_plural = 'Stawki VAT'


@six.python_2_unicode_compatible
class Group(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'grupa towarowa'
        verbose_name_plural = 'grupy towarowe'

    def __str__(self):
        return self.name


class Product(models.Model):
    owner = models.ForeignKey('userprofile.BusinessEntity')
    code = models.CharField(max_length=32, null=True, blank=True, unique=True)
    group = models.ForeignKey(Group, null=True, blank=True)
    name = models.CharField(max_length=255)
    desc = models.TextField(null=True, blank=True)
    price_net = models.DecimalField(max_digits=22, decimal_places=2)
    price_gross = models.DecimalField(max_digits=22, decimal_places=2)
    tax = models.ForeignKey('tax')
    unit = models.ForeignKey('unit')
    service = models.BooleanField()
    pkwiu = models.CharField(max_length=16, null=True, blank=True)
    notes = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Towar i usługa'
        verbose_name_plural = u'Towary i usługi'
