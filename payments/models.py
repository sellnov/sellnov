from django.db import models


class PaymentType(models.Model):
    name = models.CharField(max_length=64)
    transfer = models.BooleanField()
    due_days = models.PositiveIntegerField(null=True, blank=True)


