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

    def clean(self):
        data = super(LineForm, self).clean()

        value = data['product_name']
        if not value and data.get('product'):
            value = data['product'].name
        if not value:
            raise forms.ValidationError('Required')
        data['product_name'] = value

        value = data['price_net']
        if not value and data.get('product'):
            value = data['product'].price_net
        if not value:
            raise forms.ValidationError('Required')
        data['price_net'] = value

        value = data['pkwiu']
        if not value and data.get('product'):
            value = data['product'].pkwiu
        data['pkwiu'] = value

        value = data['unit']
        if not value and data.get('product'):
            value = data['product'].unit
        if not value:
            raise forms.ValidationError('Required')
        data['unit'] = value

        value = data['unit'].name
        if not value and data.get('product'):
            value = data['product'].unit.name
        if not value:
            raise forms.ValidationError('Required unit')
        data['unit_name'] = value

        value = data['tax']
        if not value and data.get('product'):
            value = data['product'].tax
        data['tax'] = value

        if 'tax' in data:
            value = data['tax'].rate
        elif data.get('product'):
            value = data['product'].tax.rate
        if value is None:
            raise forms.ValidationError('Required tax rate')

        data['tax_rate'] = value

        data['tax_value'] = data['price_net']*data['tax_rate']*data['quantity']

        value = data['price_gross']
        if not value and 'price_net' in data and 'tax_rate' in data:
            value = data['price_net']*(1+data['tax_rate'])
        if not value:
            raise forms.ValidationError('Required')
        data['price_gross'] = value

        value = data['total_net']
        data['total_net'] = data['price_net']*data['quantity']

        value = data['total_gross']
        if 'tax_rate' in data:
            value = data['total_net']*(1+data['tax_rate'])
        data['total_gross'] = value

        return data


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
