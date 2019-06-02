# encoding: utf-8

import six
from django.db import models

# Create your models here.


@six.python_2_unicode_compatible
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
    iban = models.CharField(max_length=33)

    owner = models.OneToOneField('auth.User', related_name='business_entity')
    employers = models.ManyToManyField('auth.User', related_name='works_in')

    class Meta:
        verbose_name = 'Podmiot gospodarczy'
        verbose_name_plural = 'Podmioty gospodarcze'

    def __str__(self):
        return self.name


@six.python_2_unicode_compatible
class Role(models.Model):
    name = models.CharField(max_length=64, verbose_name='nazwa')
    manhour_price = models.PositiveIntegerField(
                    verbose_name=u'cena sprzedaży roboczogodziny')

    class Meta:
        verbose_name = 'rola'
        verbose_name_plural = 'role'

    def __str__(self):
        return self.name


@six.python_2_unicode_compatible
class AssociateRoleCosts(models.Model):
    role = models.ForeignKey(
            Role, on_delete=models.CASCADE,
            verbose_name='rola')
    associate = models.ForeignKey(
            'userprofile.Associate', on_delete=models.CASCADE,
            verbose_name=u'współpracownik')
    manhour_cost = models.PositiveIntegerField(
            verbose_name='koszt roboczogodziny')

    def __str__(self):
        return u'%s (%s): %szł' % (
                self.associate, self.role, self.manhour_cost)


@six.python_2_unicode_compatible
class Associate(models.Model):
    user = models.ForeignKey(
            'auth.User', null=True, blank=True, on_delete=models.SET_NULL,
            verbose_name='konto')
    name = models.CharField(max_length=120, verbose_name='nazwisko')
    roles = models.ManyToManyField(
            Role, through=AssociateRoleCosts,
            verbose_name='role')
    default_manhour_cost = models.PositiveIntegerField(
            verbose_name=u'domyślny koszt roboczogodziny')

    class Meta:
        verbose_name = u'współpracownik'
        verbose_name_plural = u'współpracownicy'

    def __str__(self):
        return self.name
