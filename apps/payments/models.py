# encoding: utf-8

from django.conf import settings
from django.db import models


class PaymentTypeManager(models.Manager):
    def get_default(self):
        return self.get_queryset().get(name=settings.DEFAULT_PAYMENT_TYPE)

    def get_default_for_cash(self):
        try:
            return self.get_queryset().filter(transfer=False)[0]
        except IndexError:
            return None


class PaymentType(models.Model):
    name = models.CharField(max_length=64)
    transfer = models.BooleanField()
    due_days = models.PositiveIntegerField(null=True, blank=True)
    objects = PaymentTypeManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Sposób płatności'
        verbose_name_plural = u'Sposoby płatności'


class Operation(models.Model):
    document = models.ForeignKey(
        'documents.Document', related_name='payment_operations',
        on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    title = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField()
    internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
