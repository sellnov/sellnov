# encoding: utf-8

from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Jednostka miary'
        verbose_name_plural = 'Jednostki miary'


class Tax(models.Model):
    name = models.CharField(max_length=32)
    rate = models.DecimalField(max_digits=3, decimal_places=2)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Stawka VAT'
        verbose_name_plural = 'Stawki VAT'


class Product(models.Model):
    owner = models.ForeignKey('userprofile.BusinessEntity')
    name = models.CharField(max_length=255)
    desc = models.TextField(null=True, blank=True)
    price_net = models.DecimalField(max_digits=22, decimal_places=2)
    price_gross = models.DecimalField(max_digits=22, decimal_places=2)
    tax = models.ForeignKey('tax')
    unit = models.ForeignKey('unit')
    service = models.BooleanField()
    pkwiu = models.CharField(max_length=16, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Towar/usługa'
        verbose_name_plural = u'Towary/usługi'
