# coding: utf-8
"""
This is a module docstring
"""

__author__ = "Marcin Nowak"
__copyright__ = "Copyright 2013"
__license__ = "Propertiary"
__maintainer__ = "Marcin Nowak"
__email__ = "marcin.j.nowak@gmail.com"

from django.contrib import admin
from django.conf.urls import patterns, url
from django.db.models import Sum
from django.http import HttpResponse
from django import forms
from models import (
        SaleInvoice, PurchaseInvoice, SaleReceipt, ProFormaInvoice,
        AdvanceInvoice)

from documents.models import Line
import filesanitize


class LineForm(forms.ModelForm):
    price_gross = forms.DecimalField(label='Cena brutto', required=False,
            widget=forms.TextInput(attrs={'size': 8, 'disabled': True}))
    price_net = forms.DecimalField(label='Cena netto', required=False,
            widget=forms.TextInput(attrs={'size': 8 }))
    product_name = forms.CharField(label=u'Produkt/usługa', required=False,
            widget=forms.Textarea(attrs={'cols': 20, 'rows': 4}))
    unit_name = forms.CharField(label=u'Jedn.', required=False,
            widget=forms.TextInput(attrs={'size': 4,'disabled': True}))
    total_net = forms.DecimalField(label=u'Wart.netto', required=False,
            widget=forms.TextInput(attrs={'size': 10, 'disabled': True}))
    total_gross = forms.DecimalField(label=u'Wart.brutto', required=False,
            widget=forms.TextInput(attrs={'size': 10, 'disabled': True}))
    tax_value = forms.DecimalField(label=u'VAT', required=False,
            widget=forms.TextInput(attrs={'size': 5, 'disabled': True}))
    tax_rate = forms.DecimalField(label=u'Stawka', required=False,
            widget=forms.TextInput(attrs={'size': 3, 'disabled': True}))
    quantity = forms.DecimalField(label=u'Ilość', required=True,
            widget=forms.TextInput(attrs={'size': 5}))

    class Meta:
        model = Line
        fields = ('product', 'product_name', 'pkwiu', 'unit_name', 'unit',
                'price_net', 'quantity', 'tax', 'tax_rate', 'tax_value',
                'price_gross', 'total_net', 'total_gross')

    def clean(self):
        data = super(LineForm, self).clean()

        if self.instance:
            old = type(self.instance).objects.get(pk=self.instance.pk)
        else:
            old = None

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

        adv_net, adv_gross = data.get('advance_payment_net'), data.get('advance_payment_gross')

        if adv_net or adv_gross:
            if old:
                if (not old.advance_payment_net == adv_net and
                        old.advance_payment_gross == adv_gross):
                    # zmienilo sie netto, wyliczamy brutto
                    data['advance_payment_gross'] = adv_net*(1+data['tax_rate'])
                elif (not old.advance_payment_gross == adv_gross and
                        old.advance_payment_net == adv_net):
                    # zmienilo sie brutto, wyliczamy netto
                    data['advance_payment_net'] = adv_gross/(1+data['tax_rate'])
                else:
                    # liczymy zawsze od netto, bo nie ufamy userowi
                    data['advance_payment_gross'] = adv_net*(1+data['tax_rate'])
            else:
                if adv_gross and not adv_net:
                    # user podal brutto, wyliczamy netto
                    data['advance_payment_net'] = adv_gross/(1+data['tax_rate'])
                else:
                    # user podal netto lub obie, wyliczamy brutto
                    data['advance_payment_net'] = adv_gross/(1+data['tax_rate'])

        return data


class AdvancePaymentLineForm(LineForm):
    advance_payment_net = forms.DecimalField(
            label=u'Zaliczka netto', required=False,
            widget=forms.TextInput(attrs={'size': 5}))
    advance_payment_gross = forms.DecimalField(
            label=u'Zaliczka brutto', required=False,
            widget=forms.TextInput(attrs={'size': 5}))


class LineAdmin(admin.TabularInline):
    model = Line
    form = LineForm
    fields = (
            'product', 'product_name', 'pkwiu', 'unit', 'unit_name',
            'price_net', 'quantity', 'tax', 'tax_rate', 'price_gross',
            'total_net', 'tax_value', 'total_gross',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'product_name':
            kwargs['widget'] = forms.Textarea(attrs={'rows': 4})
        elif db_field.name in (
                'pkwiu', 'price_net', 'price_gross',
                'total_net', 'total_gross', 'quantity', 'tax_value'):
            kwargs['widget'] = forms.TextInput(attrs={'size': 10})
        return super(LineAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class DocumentAdmin(admin.ModelAdmin):
    inlines = [LineAdmin]
    list_display = [
            'number_fmt', 'customer', 'total_net', 'total_vat',
            'total_gross', 'operation_date', 'issue_date', 'pay_date', 'paid']

    def total_net(self, obj):
        return obj.line_set.aggregate(Sum('total_net'))['total_net__sum']

    def total_gross(self, obj):
        return obj.line_set.aggregate(Sum('total_gross'))['total_gross__sum']

    def total_vat(self, obj):
        return obj.line_set.aggregate(Sum('tax_value'))['tax_value__sum']

    def print_document(self, request, object_id):
        invoice = self.get_object(request, object_id)
        pdf = invoice.as_pdf({'copy': request.GET.get('copy')})
        copy = '_kopia' if request.GET.get('copy') else ''
        filename = filesanitize.safe_path('%s_%s%s.pdf' % (
            invoice._meta.verbose_name, invoice.number_fmt, copy))
        resp = HttpResponse(content=pdf.read(), content_type='application/pdf')
        resp['Content-Disposition']='filename=%s' % filename
        return resp

    def get_urls(self):
        urls = super(DocumentAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(.+)/print/$',
                admin.site.admin_view(self.print_document),
                name='document_print'),
            )
        return my_urls + urls

    def get_queryset(self, request):
        return super(DocumentAdmin, self).get_queryset(request).filter(
                doctype=self.model._meta.model_name)


class AdvancePaymentLineAdmin(LineAdmin):
    form = AdvancePaymentLineForm
    fields = list(LineAdmin.fields)+[
            'advance_payment_net', 'advance_payment_gross']


class SaleInvoiceAdmin(DocumentAdmin):
    pass


class PurchaseInvoiceAdmin(DocumentAdmin):
    pass


class SaleReceiptAdmin(DocumentAdmin):
    pass


class ProFormaInvoiceAdmin(DocumentAdmin):
    pass


class AdvanceInvoiceAdmin(DocumentAdmin):
    inlines = [AdvancePaymentLineAdmin]


admin.site.register(SaleInvoice, SaleInvoiceAdmin)
admin.site.register(PurchaseInvoice, PurchaseInvoiceAdmin)
admin.site.register(SaleReceipt, SaleReceiptAdmin)
admin.site.register(ProFormaInvoice, ProFormaInvoiceAdmin)
admin.site.register(AdvanceInvoice, AdvanceInvoiceAdmin)
