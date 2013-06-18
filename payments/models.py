# encoding: utf-8

from django.db import models


class PaymentType(models.Model):
    name = models.CharField(max_length=64)
    transfer = models.BooleanField()
    due_days = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Sposób płatności'
        verbose_name_plural = u'Sposoby płatności'
