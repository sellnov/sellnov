# coding: utf-8

import datetime

from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.db.models import Sum
from django.http import HttpResponse
from django import forms
from payments.models import PaymentType
from .forms import LineForm, SaleInvoiceForm
from .models import (
        SaleInvoice, PurchaseInvoice, SaleReceipt, ProFormaInvoice,
        AdvanceInvoice)

from documents.models import Line
import filesanitize


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
        resp['Content-Disposition'] = 'filename=%s' % filename
        return resp

    def get_urls(self):
        urls = super(DocumentAdmin, self).get_urls()
        my_urls = [
            path(
                '<int:object_id>/print/',
                admin.site.admin_view(self.print_document))
            ]
        return list(my_urls) + urls

    def get_queryset(self, request):
        return super(DocumentAdmin, self).get_queryset(request).filter(
                doctype=self.model._meta.model_name)


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
