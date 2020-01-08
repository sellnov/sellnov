# coding: utf-8

import itertools

from django.contrib import admin
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.translation import ugettext_lazy as _
from invoices.admin import LineForm
from stock.models import Tax, Unit

from .models import Entry, Valuation, ValuationItem


class BooleanRelatedFieldFilter(admin.BooleanFieldListFilter):
    def queryset(self, request, queryset):
        if self.lookup_val == '1':
            return queryset.filter(**{'%s__isnull' % self.field_path: False})
        elif self.lookup_val == '0':
            return queryset.filter(**{'%s__isnull' % self.field_path: True})
        return queryset

    def choices(self, changelist):
        for lookup, title in (
                (None, _('All')),
                ('1', _('Wystawione')),
                ('0', _('Nie wystawione'))):
            yield {
                'selected': self.lookup_val == lookup and not self.lookup_val2,
                'query_string': changelist.get_query_string({
                    self.lookup_kwarg: lookup}, [self.lookup_kwarg2]),
                'display': title,
            }


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
            'title', 'customer', 'ticket', 'associate_role',
            'price', 'cost', 'profit',
            'duration', 'work_finished_at', 'invoice', 'invoiced', 'paid')
    list_filter = (
            ('invoice', BooleanRelatedFieldFilter),
            ('customer', admin.RelatedOnlyFieldListFilter),
            ('associate_role', admin.RelatedOnlyFieldListFilter),
            )
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


class ValuationItemsInline(admin.TabularInline):
    model = ValuationItem
    readonly_fields = ('min_price', 'max_price')
    fields = (
        'name', 'role', 'min_hours', 'max_hours',
        'min_price', 'max_price',
        'proposed_price', 'notes')

    def min_price(self, obj):
        return obj.min_price()

    def max_price(self, obj):
        return obj.max_price()


@admin.register(Valuation)
class ValuationAdmin(admin.ModelAdmin):
    inlines = [ValuationItemsInline]
    list_display = ('title', 'customer', 'date', 'expiration_date')

    def preview(self, request, object_id):
        instance = self.get_queryset(request).get(pk=object_id)
        return render(
                request,
                'admin/worklog/valuation_preview.html', {
                    'title': 'Podgląd wyceny',
                    'admin_site': self.admin_site.name,
                    'opts': self.model._meta,
                    'app_label': self.model._meta.app_label,
                    'object': instance,
                    'original': instance,
                    'has_change_permission': False,
                    })

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                '<int:object_id>/preview/',
                self.admin_site.admin_view(self.preview)),
            ]
        return my_urls + urls
