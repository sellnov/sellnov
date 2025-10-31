import datetime

import filesanitize
from django import forms
from django.contrib import admin
from django.db.models import Sum
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.urls import path
from django.utils import timezone

from .forms import AddDocumentForm, LineForm
from .models import DocumentCustomer, DocumentOwner, Line


class DocumentCustomerInline(admin.StackedInline):
    model = DocumentCustomer


class DocumentOwnerInline(admin.StackedInline):
    model = DocumentOwner


class LineAdmin(admin.TabularInline):
    model = Line
    form = LineForm
    fields = (
        "line_number",
        "product",
        "product_name",
        "pkwiu",
        "unit",
        "unit_name",
        "price_net",
        "quantity",
        "tax",
        "tax_rate",
        "price_gross",
        "total_net",
        "tax_value",
        "total_gross",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(editable=True)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "product_name":
            kwargs["widget"] = forms.Textarea(attrs={"rows": 4})
        elif db_field.name in (
            "pkwiu",
            "price_net",
            "price_gross",
            "total_net",
            "total_gross",
            "quantity",
            "tax_value",
        ):
            kwargs["widget"] = forms.TextInput(attrs={"size": 10})
        return super(LineAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class DocumentAdmin(admin.ModelAdmin):
    inlines = [LineAdmin, DocumentCustomerInline, DocumentOwnerInline]
    list_display = [
        "number_fmt",
        "customer",
        "total_net",
        "total_vat",
        "total_gross",
        "operation_date",
        "issue_date",
        "pay_date",
        "paid",
        "paid_at",
    ]
    ordering = ("-issue_date",)

    def total_net(self, obj):
        return obj.line_set.aggregate(Sum("total_net"))["total_net__sum"]

    def total_gross(self, obj):
        return obj.line_set.aggregate(Sum("total_gross"))["total_gross__sum"]

    def total_vat(self, obj):
        return obj.line_set.aggregate(Sum("tax_value"))["tax_value__sum"]

    def print_document(self, request, object_id):
        invoice = self.get_object(request, object_id)
        pdf = invoice.as_pdf({"copy": request.GET.get("copy")})
        copy = "_kopia" if request.GET.get("copy") else ""
        filename = filesanitize.safe_path(
            "%s_%s%s.pdf" % (invoice._meta.verbose_name, invoice.number_fmt, copy)
        )
        resp = HttpResponse(content=pdf.read(), content_type="application/pdf")
        resp["Content-Disposition"] = "filename=%s" % filename
        return resp

    def get_urls(self):
        urls = super(DocumentAdmin, self).get_urls()
        my_urls = [
            path("<int:object_id>/print/", admin.site.admin_view(self.print_document))
        ]
        return list(my_urls) + urls

    def get_queryset(self, request):
        return super(DocumentAdmin, self).get_queryset(request)

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            try:
                add_form = self.add_form
            except AttributeError:
                add_form = forms.modelform_factory(self.model, form=AddDocumentForm)
            kwargs["form"] = add_form
        return super(DocumentAdmin, self).get_form(request, obj=obj, **kwargs)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        today = timezone.now().date()
        selected_owner = request.user.business_entity
        initial.setdefault("selected_owner", selected_owner.pk)
        initial.setdefault("issue_date", today)
        initial.setdefault("operation_date", today)
        return initial

    def get_add_inline_instances(self, request):
        return getattr(self, "add_inlines", [])

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return self.get_add_inline_instances(request)
        else:
            return super(DocumentAdmin, self).get_inline_instances(request, obj)

    def save_model(self, request, obj, form, change):

        if obj.number is None:
            obj.number = type(obj).acquire_number(
                obj.selected_owner, date=obj.issue_date
            )

        if not obj.number_fmt:
            obj.number_fmt = obj.get_formatted_number()

        if not obj.issuer_name and request.user.get_full_name():
            obj.issuer_name = request.user.get_full_name()

        ret = super(DocumentAdmin, self).save_model(request, obj, form, change)

        if obj.paid and not obj.paid_at:
            obj.paid_at = datetime.date.today()

        """
        if change:
            prev = type(obj).get(pk=obj.pk)
        else:
            prev = None

        if obj.paid and (not prev or not prev.paid):
            if obj.paid and not obj.paid_at:
                obj.paid_at = datetime.date.today()
                obj.save(update_fields=['paid_at'])

            obj.payment_operations.create(
                amount=obj.total_gross(),
                internal=True,
                date=obj.paid_at,
                title="Rozliczenie automatyczne"
            )

        if not obj.paid and prev and prev.paid:
            obj.paid_at = None
            obj.save(update_fields=['paid_at'])
            obj.payment_operations.filter(internal=True).delete()
        """

        if not change:
            customer = form.cleaned_data["selected_customer"]
            owner = form.cleaned_data["selected_owner"]

            customer_data = model_to_dict(customer)
            customer_data.pop("id", None)
            customer_data.pop("pk", None)
            customer_data["customer"] = customer
            customer_data["document"] = obj
            customer_data["owner"] = owner
            DocumentCustomer.objects.create(**customer_data)

            owner_data = model_to_dict(owner)
            owner_data.pop("id", None)
            owner_data.pop("pk", None)
            owner_data.pop("employers", None)
            owner_data["document"] = obj
            owner_data["owner"] = owner
            DocumentOwner.objects.create(**owner_data)

        return ret
