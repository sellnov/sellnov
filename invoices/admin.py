# coding: utf-8

import datetime

from django.contrib import admin
from django.conf import settings
from django import forms
from documents.admin import LineAdmin, DocumentAdmin
from documents.forms import LineForm
from payments.models import PaymentType
from .forms import SaleInvoiceForm
from .models import (
        SaleInvoice, PurchaseInvoice, SaleReceipt, ProFormaInvoice,
        AdvanceInvoice)


class AdvancePaymentLineForm(LineForm):
    advance_payment_net = forms.DecimalField(
            label=u'Zaliczka netto', required=False,
            widget=forms.TextInput(attrs={'size': 5}))
    advance_payment_gross = forms.DecimalField(
            label=u'Zaliczka brutto', required=False,
            widget=forms.TextInput(attrs={'size': 5}))


class AdvancePaymentLineAdmin(LineAdmin):
    form = AdvancePaymentLineForm
    fields = list(LineAdmin.fields)+[
            'advance_payment_net', 'advance_payment_gross']


@admin.register(SaleInvoice)
class SaleInvoiceAdmin(DocumentAdmin):
    form = SaleInvoiceForm
    readonly_fields = ('number',)

    def save_model(self, request, obj, form, change):
        if obj.number is None:
            obj.number = type(obj).acquire_number(date=obj.issue_date)

        if not obj.number_fmt:
            obj.number_fmt = obj.get_formatted_number()

        return super(SaleInvoiceAdmin, self).save_model(
                                        request, obj, form, change)

    def get_changeform_initial_data(self, request):
        data = super(
            SaleInvoiceAdmin, self).get_changeform_initial_data(request)
        if 'location' not in data:
            data['location'] = request.user.business_entity.city
        if 'payment_type' not in data:
            data['payment_type'] = PaymentType.objects.get_default().pk
        if 'issue_date' not in data:
            data['issue_date'] = datetime.date.today()
        if 'operation_date' not in data:
            data['operation_date'] = datetime.date.today()
        if 'pay_date' not in data:
            data['pay_date'] = data['issue_date'] + datetime.timedelta(
                                        days=settings.DEFAULT_PAYMENT_DAYS)
        if 'owner' not in data:
            data['owner'] = request.user.business_entity.pk

        return data


class PurchaseInvoiceAdmin(DocumentAdmin):
    pass


class SaleReceiptAdmin(DocumentAdmin):
    pass


class ProFormaInvoiceAdmin(DocumentAdmin):
    pass


class AdvanceInvoiceAdmin(DocumentAdmin):
    inlines = [AdvancePaymentLineAdmin]


admin.site.register(PurchaseInvoice, PurchaseInvoiceAdmin)
admin.site.register(SaleReceipt, SaleReceiptAdmin)
admin.site.register(ProFormaInvoice, ProFormaInvoiceAdmin)
admin.site.register(AdvanceInvoice, AdvanceInvoiceAdmin)
