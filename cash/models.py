from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Operation(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=64)
    estimated_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    draft = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date', '-created')

    def __unicode__(self):
        return u'%s: %s (%s)' % (self.date, self.title, self.estimated_amount)


class Transfer(models.Model):
    account = models.ForeignKey(Account)
    operation = models.ForeignKey(Operation)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class TransferWithBalance(models.Model):
    account = models.ForeignKey(Account)
    operation = models.ForeignKey(Operation)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'cash_transfer_with_balance_view'


class MonthlyTransferBalance(models.Model):
    year = models.PositiveIntegerField(primary_key=True)
    month = models.PositiveIntegerField(primary_key=True)
    account = models.ForeignKey(Account)
    sum_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'cash_transfer_monthly_view'
