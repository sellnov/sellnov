from django.contrib import admin
from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
            'title', 'customer', 'ticket', 'associate_role',
            'price', 'cost', 'profit',
            'duration', 'work_finished_at', 'paid')
    list_filter = ('paid', 'customer', 'associate_role')

    def duration(self, obj):
        return obj.duration()

    def cost(self, obj):
        return obj.calc_cost()

    def profit(self, obj):
        return obj.calc_profit()
