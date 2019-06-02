# encoding: utf-8

from django.db import models

CUSTOMER_TYPE_CHOICES = (
       (0, 'Dostawca/Odbiorca'),
       (1, 'Dostawca'),
       (2, 'Odbiorca'),
)

class Customer(models.Model):
    owner = models.ForeignKey('userprofile.BusinessEntity')
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=8)
    city = models.CharField(max_length=64)
    nip = models.CharField(max_length=16, blank=True)
    regon = models.CharField(max_length=8, blank=True, default='')
    phone = models.CharField(max_length=64, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    www = models.URLField(max_length=255, null=True, blank=True)
    custtype = models.IntegerField(choices=CUSTOMER_TYPE_CHOICES)
    default_manhour_price = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Klient'
        verbose_name_plural = 'Klienci'
