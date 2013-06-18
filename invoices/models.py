# encoding: utf-8

from django.db import models
from django.db.models import Sum


class SaleInvoice(models.Model):
    customer = models.ForeignKey('customers.Customer', verbose_name='Klient')
    seller = models.ForeignKey('userprofile.BusinessEntity', verbose_name='Sprzedawca')
    sell_date = models.DateField(u'Data sprzedaży')
    issue_date = models.DateField(u'Data wystawienia')
    pay_date = models.DateField(u'Termin płatności')
    location = models.CharField(u'Miejsce wystawienia', max_length=128)
    number = models.PositiveIntegerField('Numer')
    number_fmt = models.CharField(u'Numer wyświetlany', max_length=32)
    payment_type = models.ForeignKey('payments.PaymentType', verbose_name=u'Sposób płatności')
    payment_name = models.CharField(u'Nazwa płatności', max_length=128)
    comment = models.TextField('Komentarz', null=True, blank=True)
    issuer_name = models.CharField(u'Osoba wystawiająca', max_length=128, blank=True, default='')
    paid = models.BooleanField(u'Zapłacona', default=False)

    class Meta:
        verbose_name = 'Faktura sprzedaży'
        verbose_name_plural = 'Faktury sprzedaży'

    def __unicode__(self):
        return self.number_fmt

    @property
    def issue_city(self):
        return self.seller.city # fixme

    def total_unpaid(self):
        return 0 if self.paid else self.total_gross()

    def total_paid(self):
        return 0 if not self.paid else self.total_gross()

    def pay_date_days(self):
        return (self.pay_date-self.sell_date).days

    @property
    def currency(self):
        return u'zł'

    def as_pdf(self, extra_context=None):
        import sellnov.pdf
        return sellnov.pdf.create_pdf(self, 'rml/sale_invoice.rml',
                extra_context=extra_context)

    def total_tax_value(self):
        try:
            return self.saleinvoiceline_set.aggregate(Sum('tax_value'))['tax_value__sum']
        except KeyError:
            return 0

    def total_net(self):
        try:
            return self.saleinvoiceline_set.aggregate(Sum('total_net'))['total_net__sum']
        except KeyError:
            return 0

    def total_gross(self):
        try:
            return self.saleinvoiceline_set.aggregate(Sum('total_gross'))['total_gross__sum']
        except KeyError:
            return 0

    def tax_summary(self):
        return self.saleinvoiceline_set.values('tax__name').annotate(
                total_gross=Sum('total_gross'),
                total_net=Sum('total_net'),
                tax_value=Sum('tax_value'))

    def issuer_full_name(self):
        return self.seller.owner.get_full_name()

    def receiver_full_name(self):
        return ''


class SaleInvoiceLine(models.Model):
    invoice = models.ForeignKey(SaleInvoice)
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

    @property
    def tax_rate_prc(self):
        return '%s%%' % int(self.tax_rate*100)


