# encoding: utf-8

from django.conf import settings
from django.db import models


class PaymentTypeManager(models.Manager):
    def get_default(self):
        return self.get_queryset().get(name=settings.DEFAULT_PAYMENT_TYPE)


class PaymentType(models.Model):
    name = models.CharField(max_length=64)
    transfer = models.BooleanField()
    due_days = models.PositiveIntegerField(null=True, blank=True)
    objects = PaymentTypeManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Sposób płatności'
        verbose_name_plural = u'Sposoby płatności'
