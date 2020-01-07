# coding: utf-8

import decimal
import datetime
from django.db import models
from django.db.models import Sum
from customers.models import PriceList


UNITS_TO_SECONDS = {
        'm': lambda x: x*60,
        'h': lambda x: x*3600,
        'd': lambda x: x*86400,
        }


class Entry(models.Model):
    """A work done entry"""

    UNIT_CHOICES = (
            ('m', 'minut'),
            ('h', 'godzin'),
            ('d', 'dni'),
            )

    customer = models.ForeignKey(
            'customers.Customer', on_delete=models.PROTECT)
    ticket = models.ForeignKey(
            'tickets.Ticket', on_delete=models.PROTECT,
            null=True, blank=True)
    associate_role = models.ForeignKey(
            'userprofile.AssociateRoleCosts', null=True, blank=True,
            on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    time = models.DecimalField(decimal_places=1, max_digits=6)
    unit = models.CharField(
            max_length=3, choices=UNIT_CHOICES, default='h')
    price = models.DecimalField(decimal_places=2, max_digits=10)

    work_finished_at = models.DateField()
    work_started_at = models.DateField(null=True, blank=True)

    invoice = models.ForeignKey(
            'invoices.SaleInvoice', null=True, blank=True,
            on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'wykonana praca'
        verbose_name_plural = 'wykonane prace'

    def duration(self):
        return datetime.timedelta(
                seconds=int(UNITS_TO_SECONDS[self.unit](float(self.time))))

    def duration_hours(self):
        return self.duration().total_seconds()/3600.0

    @property
    def associate(self):
        return self.associate_role.associate if self.associate_role else None

    def calc_cost(self):
        if self.associate_role:
            return decimal.Decimal(str(
                    self.associate_role.manhour_cost))*decimal.Decimal(
                                            str(self.duration_hours()))

    def calc_profit(self):
        if self.associate_role:
            return self.price - self.calc_cost()


class Valuation(models.Model):
    customer = models.ForeignKey(
            'customers.Customer', on_delete=models.PROTECT,
            verbose_name='klient')
    ticket = models.ForeignKey(
            'tickets.Ticket', null=True, blank=True,
            on_delete=models.SET_NULL)
    title = models.CharField(max_length=128, verbose_name=u'tytuł oferty')
    date = models.DateField(verbose_name='data wyceny')
    expiration_date = models.DateField(verbose_name=u'ważność wyceny')
    implementation_days = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=False, blank=True, default='')
    notes = models.TextField(null=False, blank=True, default='')

    class Meta:
        verbose_name = 'wycena'
        verbose_name_plural = 'wyceny'

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_min_hours(self):
        return self.valuationitem_set.aggregate(
                Sum('min_hours'))['min_hours__sum']

    def total_max_hours(self):
        return self.valuationitem_set.aggregate(
                Sum('max_hours'))['max_hours__sum']

    def price_for_role(self, role):
        try:
            price = self.customer.pricelist_set.get(role=role).manhour_price
        except PriceList.DoesNotExist:
            price = self.customer.default_manhour_price
        return price or 0

    def total_proposed_price(self):
        return self.valuationitem_set.aggregate(
                Sum('proposed_price'))['proposed_price__sum']


class ValuationItem(models.Model):
    valuation = models.ForeignKey(
            Valuation, verbose_name='wycena', on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='opis prac / etapu')
    role = models.ForeignKey(
            'userprofile.Role', verbose_name='rola',
            on_delete=models.PROTECT)
    min_hours = models.PositiveIntegerField(verbose_name='min godziny')
    max_hours = models.PositiveIntegerField(verbose_name='max godziny')
    proposed_price = models.DecimalField(
            decimal_places=2, max_digits=10, null=True, blank=True)
    notes = models.CharField(
            max_length=255, null=False, blank=True,
            verbose_name='uwagi')

    class Meta:
        verbose_name = 'element wyceny'
        verbose_name_plural = 'elementy wyceny'

    def min_price(self):
        price = self.valuation.price_for_role(self.role)
        return self.min_hours * price

    def max_price(self):
        price = self.valuation.price_for_role(self.role)
        return self.max_hours * price
