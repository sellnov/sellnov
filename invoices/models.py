# encoding: utf-8

from documents.models import Document, Line


class SaleInvoice(Document):
    @property
    def sell_date(self):
        return self.operation_date

    @property
    def seller(self):
        return self.owner

    @property
    def buyer(self):
        return self.customer

    def advance_invoices(self):
        return self.related_documents().filter(doctype='advanceinvoice')

    def is_final_invoice(self):
        return self.advance_invoices().exists()

    def total_advance_payment_net(self):
        total = 0
        for x in self.advance_invoices():
            total += x.total_advance_payment_net()
        return total

    def total_advance_payment_gross(self):
        total = 0
        for x in self.advance_invoices():
            total += x.total_advance_payment_gross()
        return total

    def original_order_lines(self):
        """ fixme """
        if not self.is_final_invoice():
            return Line.objects.none()
        else:
            return self.original_order().lines_ordered()

    def original_order(self):
        """ fixme """
        if not self.is_final_invoice():
            return None
        else:
            return self.advance_invoices()[0]

    class Meta:
        proxy = True
        verbose_name = u'Faktura sprzedaży'
        verbose_name_plural = u'Faktury sprzedaży'


class PurchaseInvoice(Document):
    @property
    def buy_date(self):
        return self.operation_date

    @property
    def buyer(self):
        return self.owner

    @property
    def seller(self):
        return self.customer

    class Meta:
        proxy = True
        verbose_name = 'Faktura zakupu'
        verbose_name_plural = 'Faktury zakupu'


class SaleReceipt(Document):
    """
    Paragon sprzedaz
    """
    @property
    def sell_date(self):
        return self.operation_date

    @property
    def seller(self):
        return self.owner

    @property
    def buyer(self):
        return self.customer

    class Meta:
        proxy = True
        verbose_name = 'Paragon'
        verbose_name_plural = 'Paragony'


class ProFormaInvoice(Document):
    """
    Faktura pro forma
    """
    @property
    def sell_date(self):
        return self.operation_date

    @property
    def seller(self):
        return self.owner

    @property
    def buyer(self):
        return self.customer

    class Meta:
        proxy = True
        verbose_name = 'Faktura ProForma'
        verbose_name_plural = 'Faktury ProForma'


class AdvanceInvoice(Document):
    """
    Faktura zaliczkowa
    """
    @property
    def sell_date(self):
        return self.operation_date

    @property
    def seller(self):
        return self.owner

    @property
    def buyer(self):
        return self.customer

    class Meta:
        proxy = True
        verbose_name = 'Faktura zaliczkowa'
        verbose_name_plural = 'Faktury zaliczkowe'
