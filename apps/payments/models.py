# encoding: utf-8

from django.conf import settings
from django.db import models
from userprofile.models import AbstractBusinessEntity


class PaymentTypeManager(models.Manager):
    def get_default(self, business_entity: AbstractBusinessEntity):
        try:
            return business_entity.default_transfer_payment_type
        except PaymentType.DoesNotExist:
            return None

    def get_default_for_cash(self, business_entity: AbstractBusinessEntity):
        try:
            return business_entity.default_cash_payment_type
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
        verbose_name = "Sposób płatności"
        verbose_name_plural = "Sposoby płatności"


class Operation(models.Model):
    document = models.ForeignKey(
        "documents.Document",
        related_name="payment_operations",
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    title = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField()
    internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
