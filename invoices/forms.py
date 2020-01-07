# coding: utf-8

from django import forms
from customers.models import Customer
from .models import SaleInvoice


class SaleInvoiceForm(forms.ModelForm):
    selected_customer = forms.ModelChoiceField(
            queryset=Customer.objects.filter(custtype__in=(0, 2)))

    class Meta:
        model = SaleInvoice
        fields = (
            'owner', 'selected_customer', 'number', 'issue_date',
            'operation_date',
            'pay_date', 'location', 'payment_type', 'comment', 'issuer_name',
            'paid',)
