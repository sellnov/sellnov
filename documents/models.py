# encoding: utf-8

from django.db import models
from django.db.models import Sum


class Document(models.Model):
    parent = models.ForeignKey(
            'self', null=True, blank=True,
            verbose_name='Dokument powiązany (nadrzędny)')
    customer = models.ForeignKey('customers.Customer', verbose_name='Klient')
    owner = models.ForeignKey(
            'userprofile.BusinessEntity', verbose_name='Podmiot')
    operation_date = models.DateField(u'Data czynności')
    issue_date = models.DateField(u'Data wystawienia')
    pay_date = models.DateField(u'Termin płatności')
    location = models.CharField(u'Miejsce wystawienia', max_length=128)
    number = models.PositiveIntegerField('Numer')
    number_fmt = models.CharField(u'Numer wyświetlany', max_length=32)
    payment_type = models.ForeignKey(
            'payments.PaymentType', verbose_name=u'Sposób płatności')
    payment_name = models.CharField(u'Nazwa płatności', max_length=128)
    comment = models.TextField('Komentarz', null=True, blank=True)
    issuer_name = models.CharField(
            u'Osoba wystawiająca', max_length=128, blank=True, default='')
    paid = models.BooleanField(u'Zapłacona', default=False)
    doctype = models.CharField(max_length=32, editable=False)

    def __unicode__(self):
        return '%s %s' % (self.doctype, self.number_fmt)

    @property
    def issue_city(self):
        return self.seller.city  # fixme

    def total_unpaid(self):
        return 0 if self.paid else self.total_gross()

    def total_paid(self):
        return 0 if not self.paid else self.total_gross()

    def pay_date_days(self):
        return (self.pay_date-self.issue_date).days

    @property
    def currency(self):
        return u'zł'

    def as_pdf(self, extra_context=None):
        import sellnov.pdf
        return sellnov.pdf.create_pdf(
                self, '%s/%s.rml' % (self._meta.app_label, self.doctype),
                extra_context=extra_context)

    def total_tax_value(self):
        try:
            return self.line_set.aggregate(Sum('tax_value'))['tax_value__sum']
        except KeyError:
            return 0

    def total_net(self):
        try:
            return self.line_set.aggregate(Sum('total_net'))['total_net__sum']
        except KeyError:
            return 0

    def total_gross(self):
        try:
            return self.line_set.aggregate(
                    Sum('total_gross'))['total_gross__sum']
        except KeyError:
            return 0

    def tax_summary(self):
        return self.line_set.values('tax__name').annotate(
                total_gross=Sum('total_gross'),
                total_net=Sum('total_net'),
                tax_value=Sum('tax_value'))

    def advance_payment_tax_summary(self):
        return self.line_set.values('tax__name').annotate(
            total_gross=Sum('advance_payment_gross'),
            total_net=Sum('advance_payment_net'),
            tax_value=Sum('advance_payment_gross')-Sum('advance_payment_net'))

    def issuer_full_name(self):
        return self.issuer_name

    def receiver_full_name(self):
        return ''

    def save(self, *args, **kw):
        self.doctype = self._meta.model_name
        return super(Document, self).save(*args, **kw)

    def lines_ordered(self):
        return self.line_set.order_by('pk')

    def total_advance_payment_net(self):
        try:
            return self.line_set.aggregate(
                    Sum('advance_payment_net'))['advance_payment_net__sum']
        except KeyError:
            return 0

    def total_advance_payment_gross(self):
        try:
            return self.line_set.aggregate(
                    Sum('advance_payment_gross'))['advance_payment_gross__sum']
        except KeyError:
            return 0

    def total_advance_payment_tax_value(self):
        return (
                self.total_advance_payment_gross()
                - self.total_advance_payment_net())

    def total_advance_payment_unpaid_gross(self):
        """
        Kwota pozostala do zaplaty
        """
        prev_paid = 0
        for doc in self.related_documents_of_same_type():
            prev_paid += doc.total_advance_payment_gross()
        return (
                self.total_gross() - self.total_advance_payment_gross()
                - prev_paid)

    def related_documents(self):
        if self.parent:
            return Document.objects.filter(
                    parent=self.parent).exclude(pk=self.pk)
        else:
            return Document.objects.none()

    def related_documents_of_same_type(self):
        return self.related_documents().filter(doctype=self.doctype)

    def related_previous_documents_of_same_type(self):
        return self.related_documents().filter(
                doctype=self.doctype, issue_date__lte=self.issue_date)


class Line(models.Model):
    document = models.ForeignKey(Document)
    product = models.ForeignKey('stock.Product', null=True, blank=True)
    product_name = models.CharField(max_length=128)
    unit = models.ForeignKey('stock.Unit', null=True, blank=True)
    unit_name = models.CharField(max_length=32)
    price_net = models.DecimalField(max_digits=22, decimal_places=2)
    price_gross = models.DecimalField(max_digits=22, decimal_places=2)
    advance_payment_net = models.DecimalField(
            max_digits=22, decimal_places=2, default=0,
            verbose_name='Zaliczka')
    advance_payment_gross = models.DecimalField(
            max_digits=22, decimal_places=2, default=0,
            verbose_name='Zaliczka brutto')
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

    def advance_payment_tax_value(self):
        return self.advance_payment_gross-self.advance_payment_net
