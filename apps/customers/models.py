# encoding: utf-8

from django.db import models


class AbstractCustomer(models.Model):
    class Type(models.IntegerChoices):
        SUPPLIER_OR_CUSTOMER = 0, "Dostawca/Odbiorca"
        SUPPLIER = 1, "Dostawca"
        CUSTOMER = 2, "Odbiorca"

    owner = models.ForeignKey("userprofile.BusinessEntity", on_delete=models.PROTECT)
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=8)
    city = models.CharField(max_length=64)
    nip = models.CharField(max_length=16, blank=True)
    regon = models.CharField(max_length=8, blank=True, default="")
    phone = models.CharField(max_length=64, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    www = models.URLField(max_length=255, null=True, blank=True)
    custtype = models.IntegerField(choices=Type.choices)
    default_manhour_price = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self):
        return self.name


class Customer(AbstractCustomer):
    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klienci"
        ordering = ("name",)


class PriceList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    role = models.ForeignKey("userprofile.Role", on_delete=models.PROTECT)
    manhour_price = models.PositiveIntegerField()
