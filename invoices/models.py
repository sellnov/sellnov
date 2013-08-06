# encoding: utf-8

from django.db import models
from documents.models import Document


class SaleInvoice(Document):
    @property
    def sell_date(self):
        return self.operation_date

    @property
    def seller(self):
        return self.owner

    @property
    def buyer(self):
        return self.customer

    class Meta:
        proxy = True
        verbose_name = 'Faktura sprzedaży'
        verbose_name_plural = 'Faktury sprzedaży'


class PurchaseInvoice(Document):
    @property
    def buy_date(self):
        return self.operation_date

    @property
    def buyer(self):
        return self.owner

    @property
    def seller(self):
        return self.customer


    class Meta:
        proxy = True
        verbose_name = 'Faktura zakupu'
        verbose_name_plural = 'Faktury zakupu'



