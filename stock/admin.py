from django.contrib import admin
from django import forms

from .models import Product, Tax, Unit, Group


class ProductForm(forms.ModelForm):
    price_net = forms.DecimalField(required=False)
    price_gross = forms.DecimalField(required=False)

    class Meta:
        model = Product
        fields = (
                'owner', 'code', 'name', 'group', 'desc', 'price_net', 'tax',
                'price_gross', 'unit', 'service', 'pkwiu', 'notes')

    def clean(self):
        data = self.cleaned_data
        price_net = data.get('price_net')
        price_gross = data.get('price_gross')
        tax = data.get('tax')

        if price_gross is None:
            if price_net is not None and tax is not None:
                price_gross = price_net * (1+tax.rate)
        if price_net is None:
            if price_gross is not None and tax is not None:
                price_net = price_gross / (1+tax.rate)

        if price_net is None and price_gross is None:
            raise forms.ValidationError('Net or gross price is required')

        data.update({
            'price_net': price_net,
            'price_gross': price_gross,
            })

        return data


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = (
            'code', 'name', 'group', 'price_net', 'tax', 'price_gross', 'unit',
            'service', 'notes')
    list_display_links = ('code', 'name',)
    list_filter = ('service', 'group', 'unit', 'tax')
    search_fields = ('code', 'name', 'desc', 'pkwiu')
    ordering = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tax)
admin.site.register(Unit)
