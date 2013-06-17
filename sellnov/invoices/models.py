from django.db import models


class SaleInvoice(models.Model):
    customer = models.ForeignKey('customers.Customer')
    seller = models.ForeignKey('profile.Company')
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


class SaleInvoiceLine(models.Model):
    product = models.ForeignKey('stock.Product')
    product_name = models.CharField(max_length=128)
    unit = models.ForeignKey('stock.Unit')
    unit_name = models.CharField(max_length=32)
    price_net = models.DecimalField()
    price_gross = models.DecimalField()
    quantity = models.DecimalField()
    tax_value = models.DecimalField()
    total_net = models.DecimalField()
    total_gross = models.DecimalField()


