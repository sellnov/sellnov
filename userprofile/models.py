# encoding: utf-8

from django.db import models

# Create your models here.


class BusinessEntity(models.Model):
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=8)
    city = models.CharField(max_length=64)
    nip = models.CharField(max_length=16)
    regon = models.CharField(max_length=8)
    phone = models.CharField(max_length=64, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)

    bank_name = models.CharField(max_length=64)
    iban = models.CharField(max_length=32)

    owner = models.ForeignKey('auth.User')
    employers = models.ManyToManyField('auth.User', related_name='works_in')

    class Meta:
        verbose_name = 'Podmiot gospodarczy'
        verbose_name_plural = 'Podmioty gospodarcze'

    def __unicode__(self):
        return self.name

