# encoding: utf-8

import datetime

from autonumber.models import AutoNumber, format_number
from customers.models import AbstractCustomer, Customer
from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models import Sum
from payments.models import PaymentType
from userprofile.models import AbstractBusinessEntity


def class_to_doctype(cls):
    return cls._meta.label_lower


def doctype_to_class(doctype):
    return apps.get_model(doctype)


class DocumentManager(models.Manager):
    def of_class(self, document_class):
        return self.get_queryset().filter(doctype=document_class.document_type_name())

    def get_queryset(self):
        qs = super().get_queryset()

        if self.model is not Document:
            qs = qs.filter(doctype=self.model.document_type_name())

        return qs

    def create(self, **kwargs):
        if "issue_date" not in kwargs:
            kwargs["issue_date"] = datetime.date.today()
        if "pay_date" not in kwargs:
            kwargs["pay_date"] = kwargs["issue_date"] + datetime.timedelta(
                days=settings.DEFAULT_PAYMENT_DAYS
            )
        if "payment_type" not in kwargs:
            kwargs["payment_type"] = PaymentType.objects.get_default()
        kwargs["payment_name"] = kwargs["payment_type"].name

        if "location" not in kwargs and "owner" in kwargs:
            kwargs["location"] = kwargs["owner"].city
        if "number" not in kwargs and "owner" in kwargs:
            kwargs["number"] = self.model.acquire_number(
                kwargs["owner"], date=kwargs["issue_date"]
            )
        kwargs["number_fmt"] = format_number(
            self.model, kwargs["number"], kwargs["issue_date"]
        )

        return super(DocumentManager, self).create(**kwargs)


class Document(models.Model):
    AUTONUMBER_FORMAT = "%(number)s/%(year)s"
    FILTER_CUSTOMER_TYPES = None

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        verbose_name="Dokument powiązany (nadrzędny)",
        on_delete=models.PROTECT,
    )
    selected_customer = models.ForeignKey(
        "customers.Customer",
        verbose_name="Wybrany klient",
        on_delete=models.PROTECT,
        db_column="customer_id",
    )
    selected_owner = models.ForeignKey(
        "userprofile.BusinessEntity",
        verbose_name="Wybrany podmiot",
        on_delete=models.PROTECT,
    )
    operation_date = models.DateField("Data czynności")
    issue_date = models.DateField("Data wystawienia")
    pay_date = models.DateField("Termin płatności")
    location = models.CharField("Miejsce wystawienia", max_length=128)
    number = models.PositiveIntegerField("Numer")
    number_fmt = models.CharField("Numer wyświetlany", max_length=32)
    payment_type = models.ForeignKey(
        "payments.PaymentType",
        verbose_name="Sposób płatności",
        on_delete=models.PROTECT,
    )
    payment_name = models.CharField("Nazwa płatności", max_length=128)
    comment = models.TextField("Komentarz", null=True, blank=True)
    issuer_name = models.CharField(
        "Osoba wystawiająca", max_length=128, blank=True, default=""
    )
    paid = models.BooleanField("Zapłacona", default=False)
    paid_at = models.DateField(null=True, blank=True)
    doctype = models.CharField(max_length=128, editable=False, db_index=True)

    objects = DocumentManager()

    class Meta:
        ordering = ("-issue_date",)

    def __str__(self):
        cls = doctype_to_class(self.doctype)
        return f"{cls._meta.verbose_name} {self.number_fmt}"

    @classmethod
    def from_db(cls, db, field_names, values):
        doctype = values[field_names.index("doctype")]
        newcls = doctype_to_class(doctype)

        if cls == newcls:
            return super().from_db(db, field_names, values)
        else:
            return newcls.from_db(db, field_names, values)

    @property
    def issue_city(self):
        return self.seller.city  # fixme

    def total_unpaid(self):
        return 0 if self.paid else self.total_gross()

    def total_paid(self):
        return 0 if not self.paid else self.total_gross()

    def pay_date_days(self):
        return (self.pay_date - self.issue_date).days

    @property
    def currency(self):
        return "zł"

    def as_pdf(self, extra_context=None):
        import sellnov.pdf

        return sellnov.pdf.create_pdf(
            self,
            "%s/%s.rml" % (self._meta.app_label, self._meta.model_name),
            extra_context=extra_context,
        )

    def total_tax_value(self):
        try:
            return self.line_set.aggregate(Sum("tax_value"))["tax_value__sum"] or 0
        except KeyError:
            return 0

    def total_net(self):
        try:
            return self.line_set.aggregate(Sum("total_net"))["total_net__sum"] or 0
        except KeyError:
            return 0

    def total_gross(self):
        try:
            return self.line_set.aggregate(Sum("total_gross"))["total_gross__sum"] or 0
        except KeyError:
            return 0

    def tax_summary(self):
        return self.line_set.values("tax__name").annotate(
            total_gross=Sum("total_gross"),
            total_net=Sum("total_net"),
            tax_value=Sum("tax_value"),
        ).order_by()  # cancel ordering

    def advance_payment_tax_summary(self):
        return self.line_set.values("tax__name").annotate(
            total_gross=Sum("advance_payment_gross"),
            total_net=Sum("advance_payment_net"),
            tax_value=Sum("advance_payment_gross") - Sum("advance_payment_net"),
        )

    def issuer_full_name(self):
        return self.issuer_name

    def receiver_full_name(self):
        return ""

    def save(self, *args, **kw):
        self.doctype = class_to_doctype(type(self))
        return super(Document, self).save(*args, **kw)

    def lines_ordered(self):
        return self.line_set.order_by("pk")

    def total_advance_payment_net(self):
        try:
            return self.line_set.aggregate(Sum("advance_payment_net"))[
                "advance_payment_net__sum"
            ]
        except KeyError:
            return 0

    def total_advance_payment_gross(self):
        try:
            return self.line_set.aggregate(Sum("advance_payment_gross"))[
                "advance_payment_gross__sum"
            ]
        except KeyError:
            return 0

    def total_advance_payment_tax_value(self):
        return self.total_advance_payment_gross() - self.total_advance_payment_net()

    def total_advance_payment_unpaid_gross(self):
        """
        Kwota pozostala do zaplaty
        """
        prev_paid = 0
        for doc in self.related_documents_of_same_type():
            prev_paid += doc.total_advance_payment_gross()
        return self.total_gross() - self.total_advance_payment_gross() - prev_paid

    def related_documents(self):
        if self.parent:
            return Document.objects.filter(parent=self.parent).exclude(pk=self.pk)
        else:
            return Document.objects.none()

    def related_documents_of_same_type(self):
        return self.related_documents().filter(doctype=self.doctype)

    def related_previous_documents_of_same_type(self):
        return self.related_documents().filter(
            doctype=self.doctype, issue_date__lte=self.issue_date
        )

    @classmethod
    def document_type_name(cls):
        return class_to_doctype(cls)

    @classmethod
    def acquire_number(cls, business_entity, date=None):
        return AutoNumber.objects.acquire(business_entity, cls, date=date)

    def get_formatted_number(self):
        return format_number(type(self), self.number, self.issue_date)


class DocumentCustomer(AbstractCustomer):
    document = models.OneToOneField(
        Document, on_delete=models.CASCADE, related_name="customer"
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        db_table = "documents_customer"


class DocumentOwner(AbstractBusinessEntity):
    document = models.OneToOneField(
        Document, on_delete=models.CASCADE, related_name="owner"
    )
    owner = models.ForeignKey("userprofile.BusinessEntity", on_delete=models.PROTECT)

    class Meta:
        db_table = "documents_owner"


class Line(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    line_number = models.PositiveIntegerField()
    product = models.ForeignKey(
        "stock.Product", null=True, blank=True, on_delete=models.PROTECT
    )
    product_name = models.CharField(max_length=128)
    unit = models.ForeignKey(
        "stock.Unit", null=True, blank=True, on_delete=models.PROTECT
    )
    unit_name = models.CharField(max_length=32)
    price_net = models.DecimalField(max_digits=22, decimal_places=2)
    price_gross = models.DecimalField(max_digits=22, decimal_places=2)
    advance_payment_net = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, verbose_name="Zaliczka"
    )
    advance_payment_gross = models.DecimalField(
        max_digits=22, decimal_places=2, default=0, verbose_name="Zaliczka brutto"
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    tax = models.ForeignKey(
        "stock.Tax", null=True, blank=True, on_delete=models.PROTECT
    )
    tax_rate = models.DecimalField(max_digits=3, decimal_places=2)
    tax_value = models.DecimalField(max_digits=22, decimal_places=2)
    total_net = models.DecimalField(max_digits=22, decimal_places=2)
    total_gross = models.DecimalField(max_digits=22, decimal_places=2)
    pkwiu = models.CharField(max_length=64, null=True, blank=True, default="")
    comment = models.TextField(null=True, blank=True)
    related_line = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.PROTECT
    )
    editable = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ("line_number",)

    @property
    def tax_rate_prc(self):
        return "%s%%" % int(self.tax_rate * 100)

    def advance_payment_tax_value(self):
        return self.advance_payment_gross - self.advance_payment_net

    def __str__(self):
        return "%s: %s %s (%s)" % (
            self.line_number,
            self.product_name,
            self.total_net,
            self.tax_rate_prc,
        )


class SaleDocument(Document):
    FILTER_CUSTOMER_TYPES = (Customer.Type.CUSTOMER, Customer.Type.SUPPLIER_OR_CUSTOMER)

    class Meta:
        proxy = True


class PurchaseDocument(Document):
    FILTER_CUSTOMER_TYPES = (Customer.Type.SUPPLIER, Customer.Type.SUPPLIER_OR_CUSTOMER)

    class Meta:
        proxy = True
