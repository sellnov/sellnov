from django.db import models


class Customer(models.Model):
    owner = models.ForeignKey('userprofile.BusinessEntity')
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=8)
    city = models.CharField(max_length=64)
    nip = models.CharField(max_length=16)
    regon = models.CharField(max_length=8, blank=True, default='')
    phone = models.CharField(max_length=64, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    www = models.URLField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name
