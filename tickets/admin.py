from django.contrib import admin
from worklog.models import Entry
from .models import Ticket, Pricing


class PricingInlineAdmin(admin.TabularInline):
    model = Pricing


class WorkLogEntryInlineAdmin(admin.TabularInline):
    model = Entry


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    inlines = [PricingInlineAdmin, WorkLogEntryInlineAdmin]
    readonly_fields = (
            'created_at', 'updated_at', 'price_accepted_at',
            'work_accepted_at', 'started_at', 'finished_at', 'closed_at',
            )
    list_display = (
            'title_num', 'customer', 'issuer_name', 'type', 'status',
            'resolution', 'created_at',)
    list_filter = (
            'type', 'status', 'resolution',
            ('customer', admin.RelatedOnlyFieldListFilter),
            )
    search_fields = (
            'title', 'issuer_email', 'issuer_name', 'customer__name',
            'description')

    def title_num(self, obj):
        return '#%s: %s' % (obj.pk, obj.title)
    title_num.short_description = 'title'
