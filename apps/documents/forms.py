from decimal import Decimal

from django import forms

from .models import Document, Line


class AddDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = (
            "selected_owner",
            "selected_customer",
            "issue_date",
            "operation_date",
            "pay_date",
            "payment_type",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customer_types = getattr(self._meta.model, "FILTER_CUSTOMER_TYPES", None)
        customer_qs = self.fields["selected_customer"].queryset

        if customer_types:
            customer_qs = customer_qs.filter(custtype__in=customer_types)

        if self.instance and self.instance.selected_owner_id:
            owner = self.instance.selected_owner_id
        elif self.data.get("selected_owner"):
            owner = self.data.get("selected_owner")  # hmmm, not sure
        else:
            owner = self.initial.get("selected_owner")

        if owner:
            customer_qs = customer_qs.filter(owner=owner)

        self.fields["selected_customer"].queryset = customer_qs

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.payment_name = obj.payment_type.name
        obj.location = obj.selected_owner.city
        if commit:
            obj.save()
        return obj


class LineForm(forms.ModelForm):
    price_gross = forms.DecimalField(
        label="Cena brutto",
        required=False,
        widget=forms.TextInput(attrs={"size": 8, "disabled": True}),
    )
    price_net = forms.DecimalField(
        label="Cena netto", required=False, widget=forms.TextInput(attrs={"size": 8})
    )
    product_name = forms.CharField(
        label="Produkt/usługa",
        required=False,
        widget=forms.Textarea(attrs={"cols": 20, "rows": 4}),
    )
    unit_name = forms.CharField(
        label="Jedn.",
        required=False,
        widget=forms.TextInput(attrs={"size": 4, "disabled": True}),
    )
    total_net = forms.DecimalField(
        label="Wart.netto",
        required=False,
        widget=forms.TextInput(attrs={"size": 10, "disabled": True}),
    )
    total_gross = forms.DecimalField(
        label="Wart.brutto",
        required=False,
        widget=forms.TextInput(attrs={"size": 10, "disabled": True}),
    )
    tax_value = forms.DecimalField(
        label="VAT",
        required=False,
        widget=forms.TextInput(attrs={"size": 5, "disabled": True}),
    )
    tax_rate = forms.DecimalField(
        label="Stawka",
        required=False,
        widget=forms.TextInput(attrs={"size": 3, "disabled": True}),
    )
    quantity = forms.DecimalField(
        label="Ilość", required=True, widget=forms.TextInput(attrs={"size": 5})
    )

    class Meta:
        model = Line
        fields = (
            "product",
            "product_name",
            "pkwiu",
            "unit_name",
            "unit",
            "price_net",
            "quantity",
            "tax",
            "tax_rate",
            "tax_value",
            "price_gross",
            "total_net",
            "total_gross",
        )

    def clean_quantity(self):
        value = self.cleaned_data.get("quantity")
        if not value:
            value = 1
        return value

    def clean(self):
        data = self.cleaned_data

        if self.instance and self.instance.pk:
            old = type(self.instance).objects.get(pk=self.instance.pk)
        else:
            old = None

        quantity = data.get("quantity") or 1

        value = data["product_name"]
        if not value and data.get("product"):
            value = data["product"].name
        if not value:
            raise forms.ValidationError("Required")
        data["product_name"] = value

        value = data.get("price_net")
        if not value and data.get("product"):
            value = data["product"].price_net
        if not value:
            raise forms.ValidationError("Required")
        data["price_net"] = value

        value = data.get("pkwiu")

        if value is None and data.get("product"):
            value = data["product"].pkwiu or ""

        data["pkwiu"] = value

        value = data["unit"]

        if not value and data.get("product"):
            value = data["product"].unit

        if not value:
            raise forms.ValidationError("Required")
        data["unit"] = value

        value = data["unit"].name
        if not value and data.get("product"):
            value = data["product"].unit.name
        if not value:
            raise forms.ValidationError("Required unit")
        data["unit_name"] = value

        value = data["tax"]
        if not value and data.get("product"):
            value = data["product"].tax
        data["tax"] = value

        if "tax" in data:
            value = data["tax"].rate
        elif data.get("product"):
            value = data["product"].tax.rate
        if value is None:
            raise forms.ValidationError("Required tax rate")

        data["tax_rate"] = value

        data["tax_value"] = (data["price_net"] * data["tax_rate"] * quantity).quantize(
            Decimal("1.00")
        )

        value = data["price_gross"]
        if not value and "price_net" in data and "tax_rate" in data:
            value = (data["price_net"] * (1 + data["tax_rate"])).quantize(
                Decimal("1.00")
            )
        if not value:
            raise forms.ValidationError("Required")
        data["price_gross"] = value

        value = data["total_net"]
        data["total_net"] = (data["price_net"] * quantity).quantize(Decimal("1.00"))

        value = data["total_gross"]
        if "tax_rate" in data:
            value = (data["total_net"] * (1 + data["tax_rate"])).quantize(
                Decimal("1.00")
            )
        data["total_gross"] = value

        adv_net, adv_gross = (
            data.get("advance_payment_net"),
            data.get("advance_payment_gross"),
        )

        if adv_net or adv_gross:
            if old:
                if (
                    not old.advance_payment_net == adv_net
                    and old.advance_payment_gross == adv_gross
                ):
                    # zmienilo sie netto, wyliczamy brutto
                    data["advance_payment_gross"] = adv_net * (1 + data["tax_rate"])
                elif (
                    not old.advance_payment_gross == adv_gross
                    and old.advance_payment_net == adv_net
                ):
                    # zmienilo sie brutto, wyliczamy netto
                    data["advance_payment_net"] = adv_gross / (1 + data["tax_rate"])
                else:
                    # liczymy zawsze od netto, bo nie ufamy userowi
                    data["advance_payment_gross"] = adv_net * (1 + data["tax_rate"])
            else:
                if adv_gross and not adv_net:
                    # user podal brutto, wyliczamy netto
                    data["advance_payment_net"] = adv_gross / (1 + data["tax_rate"])
                else:
                    # user podal netto lub obie, wyliczamy brutto
                    data["advance_payment_net"] = adv_gross / (1 + data["tax_rate"])

        return data
