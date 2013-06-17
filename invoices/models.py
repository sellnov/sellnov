from django.db import models


class SaleInvoice(models.Model):
    customer = models.ForeignKey('customers.Customer')
    seller = models.ForeignKey('userprofile.BusinessEntity')
    sell_date = models.DateField()
    issue_date = models.DateField()
    pay_date = models.DateField()
    location = models.CharField(max_length=128)
    number = models.PositiveIntegerField()
    number_fmt = models.CharField(max_length=32)
    payment_type = models.ForeignKey('payments.PaymentType')
    payment_name = models.CharField(max_length=128)
    comment = models.TextField(null=True, blank=True)
    issuer_name = models.CharField(max_length=128, blank=True, default='')
    paid = models.BooleanField(default=False)


class SaleInvoiceLine(models.Model):
    product = models.ForeignKey('stock.Product', null=True, blank=True)
    product_name = models.CharField(max_length=128)
    unit = models.ForeignKey('stock.Unit', null=True, blank=True)
    unit_name = models.CharField(max_length=32)
    price_net = models.DecimalField(max_digits=22, decimal_places=2)
    price_gross = models.DecimalField(max_digits=22, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    tax = models.ForeignKey('stock.Tax', null=True, blank=True)
    tax_rate = models.DecimalField(max_digits=3, decimal_places=2)
    tax_value = models.DecimalField(max_digits=22, decimal_places=2)
    total_net = models.DecimalField(max_digits=22, decimal_places=2)
    total_gross = models.DecimalField(max_digits=22, decimal_places=2)
    pkwiu = models.CharField(max_length=16, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)



