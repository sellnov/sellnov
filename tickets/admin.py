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
            'title_num', 'customer', 'type', 'status', 'resolution',
            'created_at',)

    def title_num(self, obj):
        return '#%s: %s' % (obj.pk, obj.title)
    title_num.short_description = 'title'
