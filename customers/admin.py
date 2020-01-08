from django.contrib import admin
from .models import Customer, PriceList


class PriceListInline(admin.TabularInline):
    model = PriceList


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
            'name', 'custtype', 'phone', 'email', 'default_manhour_price')
    list_filter = ('custtype', 'owner', 'city')
    search_fields = ('name', 'phone', 'email', 'city', 'address')
    inlines = [PriceListInline]
