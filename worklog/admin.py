# coding: utf-8

import itertools

from django.contrib import admin
from django.db import transaction
from django.shortcuts import redirect

from stock.models import Tax, Unit
from invoices.admin import LineForm
from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
            'title', 'customer', 'ticket', 'associate_role',
            'price', 'cost', 'profit',
            'duration', 'work_finished_at', 'invoice', 'invoiced', 'paid')
    list_filter = ('customer', 'associate_role')
    actions = ['make_invoices']

    def invoiced(self, obj):
        return bool(obj.invoice)
    invoiced.boolean = True

    def paid(self, obj):
        if obj.invoice:
            return obj.invoice.paid
        else:
            return False
    paid.boolean = True

    def duration(self, obj):
        return obj.duration()

    def cost(self, obj):
        return obj.calc_cost()

    def profit(self, obj):
        return obj.calc_profit()

    @transaction.atomic
    def make_invoices(self, request, queryset):
        from invoices.models import SaleInvoice

        works_by_customer = itertools.groupby(
                        queryset, lambda x: x.customer)

        unit = Unit.objects.get_default()
        tax = Tax.objects.get_default()

        for customer, works in works_by_customer:
            works = list(works)
            operation_date = max(map(lambda x: x.work_finished_at, works))

            document = SaleInvoice.objects.create(**{
                'customer': customer,
                'operation_date': operation_date,
                'owner': request.user.business_entity,
                })

            for work in works:
                form = LineForm(data={
                    'document': document.pk,
                    'product_name': work.title,
                    'unit': unit.pk,
                    'price_net': work.price,
                    'tax': tax.pk,
                    'quantity': 1,
                    })
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.document = document
                    obj.save()
                    work.invoice = document
                    work.save()

            return redirect('admin:invoices_saleinvoice_changelist')

    make_invoices.short_description = u'Utwórz faktury dla wybranych prac'
