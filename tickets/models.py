# coding: utf-8

from django.db import models


class Enum(object):
    pass


class Type(Enum):
    ORDER = 'order'
    WARRANTY_CLAIM = 'warranty'
    ISSUE = 'issue'


class Status(Enum):
    NEW = 'new'
    PRICING = 'pricing'  # pricing and acceptance stage
    QUEUED = 'queued'  # queued to work
    INPROGRESS = 'inprogress'
    REJECTED = 'rejected'  # customer rejected (able to renegotiate)
    CLOSED = 'closed'


class Resolution(Enum):
    UNRESOLVED = 'unresolved'
    CANCELLED = 'cancelled'
    DONE = 'done'
    OVERPRICED = 'overpriced'
    NOBUDGET = 'nobudget'


class Ticket(models.Model):
    STATUS_CHOICES = (
            (Status.NEW, 'nowe'),
            (Status.PRICING, 'wycena'),
            (Status.QUEUED, 'przyjęte do realizacji'),
            (Status.INPROGRESS, 'w toku'),
            (Status.REJECTED, 'oferta odrzucona'),
            (Status.CLOSED, 'zamknięte'),
        )

    TYPE_CHOICES = (
            (Type.ORDER, 'zapotrzebowanie'),
            (Type.WARRANTY_CLAIM, 'reklamacja'),
            (Type.ISSUE, 'problem'),
        )

    RESOLUTION_CHOICES = (
            (Resolution.UNRESOLVED, 'nierozwiązane'),
            (Resolution.CANCELLED, 'anulowane'),
            (Resolution.DONE, 'zakończone'),
            (Resolution.OVERPRICED, 'zbyt wysoki koszt'),
            (Resolution.NOBUDGET, 'brak środków na realizację'),
        )

    type = models.CharField(
            max_length=16, choices=TYPE_CHOICES, db_index=True)
    status = models.CharField(
            max_length=16, choices=STATUS_CHOICES, db_index=True,
            default=Status.NEW)
    resolution = models.CharField(
            max_length=16, choices=RESOLUTION_CHOICES, db_index=True,
            default=Resolution.UNRESOLVED)

    issuer_email = models.EmailField(max_length=255, null=True, blank=True)
    issuer_name = models.CharField(max_length=255, null=True, blank=True)
    issuer = models.ForeignKey(
            'auth.User', null=True, blank=True,
            on_delete=models.SET_NULL, related_name='issued_tickets')

    customer = models.ForeignKey(
            'customers.Customer', on_delete=models.PROTECT,
            null=True, blank=True)

    title = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    issued_at = models.DateField()

    due_date = models.DateField(null=True, blank=True)
    total_price = models.DecimalField(
            max_digits=12, decimal_places=2, null=True, blank=True)
    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    price_accepted_at = models.DateTimeField(null=True, blank=True)
    price_accepted_by = models.ForeignKey(
            'auth.User', on_delete=models.PROTECT,
            related_name='price_accepted_tickets',
            null=True, blank=True)

    work_accepted_at = models.DateTimeField(null=True, blank=True)
    work_accepted_by = models.ForeignKey(
            'auth.User', on_delete=models.PROTECT,
            related_name='work_accepted_tickets',
            null=True, blank=True)

    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '#%s: %s' % (self.pk, self.title)


class Pricing(models.Model):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    ACCEPTANCE_CHOICES = (
            (ACCEPTED, 'zaakceptowana'),
            (REJECTED, 'odrzucona'),
        )

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)

    estimated_price = models.DecimalField(max_digits=10, decimal_places=2)
    accepted_price = models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=True)
    acceptance = models.CharField(
            max_length=16, choices=ACCEPTANCE_CHOICES, null=True, blank=True,
            db_index=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    accepted_by = models.ForeignKey(
            'auth.User', on_delete=models.PROTECT,
            related_name='accepted_pricings')
