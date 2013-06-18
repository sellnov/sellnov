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
from django.conf.urls.defaults import patterns, url
from django.db.models import Sum
from django.http import HttpResponse
from django import forms
from models import SaleInvoice, SaleInvoiceLine


class SaleInvoiceLineForm(forms.ModelForm):
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
        model = SaleInvoiceLine
        fields = ('product', 'product_name', 'pkwiu', 'unit_name', 'unit',
                'price_net', 'quantity', 'tax', 'tax_rate', 'tax_value',
                'price_gross', 'total_net', 'total_gross')

    def clean(self):
        data = super(SaleInvoiceLineForm, self).clean()

        value = data['product_name']
        if not value and 'product' in data:
            value = data['product'].name
        if not value:
            raise forms.ValidationError('Required')
        data['product_name'] = value

        value = data['price_net']
        if not value and 'product' in data:
            value = data['product'].price_net
        if not value:
            raise forms.ValidationError('Required')
        data['price_net'] = value


        value = data['pkwiu']
        if not value and 'product' in data:
            value = data['product'].pkwiu
        data['pkwiu'] = value

        value = data['unit']
        if not value and 'product' in data:
            value = data['product'].unit
        if not value:
            raise forms.ValidationError('Required')
        data['unit'] = value

        value = data['unit'].name
        if not value and 'product' in data:
            value = data['product'].unit.name
        if not value:
            raise forms.ValidationError('Required unit')
        data['unit_name'] = value

        value = data['tax']
        if not value and 'product' in data:
            value = data['product'].tax
        data['tax'] = value

        if 'tax' in data:
            value = data['tax'].rate
        elif 'product' in data:
            value = data['product'].tax.rate
        if value is None:
            raise forms.ValidationError('Required tax rate')

        data['tax_rate'] = value

        data['tax_value'] = data['price_net']*data['tax_rate']

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


class SaleInvoiceLineAdmin(admin.TabularInline):
    model = SaleInvoiceLine
    form = SaleInvoiceLineForm
    fields = ('product', 'product_name', 'pkwiu', 'unit', 'unit_name',
            'price_net', 'quantity', 'tax', 'tax_rate', 'price_gross',
            'total_net', 'tax_value', 'total_gross',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'product_name':
            kwargs['widget'] = forms.Textarea(attrs={'rows': 4})
        elif db_field.name in ('pkwiu', 'price_net', 'price_gross',
                'total_net', 'total_gross', 'quantity', 'tax_value'):
            kwargs['widget'] = forms.TextInput(attrs={'size': 10})
        return super(SaleInvoiceLineAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class SaleInvoiceAdmin(admin.ModelAdmin):
    inlines = [SaleInvoiceLineAdmin]
    list_display = ['number_fmt', 'customer', 'total_net', 'total_vat',
            'total_gross', 'sell_date', 'issue_date', 'pay_date', 'paid']

    def total_net(self, obj):
        return obj.saleinvoiceline_set.aggregate(Sum('total_net'))['total_net__sum']

    def total_gross(self, obj):
        return obj.saleinvoiceline_set.aggregate(Sum('total_gross'))['total_gross__sum']

    def total_vat(self, obj):
        return obj.saleinvoiceline_set.aggregate(Sum('tax_value'))['tax_value__sum']

    def print_document(self, request, object_id):
        invoice = self.get_object(request, object_id)
        pdf = invoice.as_pdf({'copy': request.GET.get('copy')})
        resp = HttpResponse(content=pdf.read(), content_type='application/pdf')
        resp['Content-Disposition']='filename=FakturaVAT_%s.pdf' % invoice.number_fmt
        return resp

    def get_urls(self):
        urls = super(SaleInvoiceAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(.+)/print/$',
                admin.site.admin_view(self.print_document),
                name='saleinvoice_print'),
            )
        return my_urls + urls



admin.site.register(SaleInvoice, SaleInvoiceAdmin)


