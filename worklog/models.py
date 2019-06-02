import decimal
import datetime
from django.db import models


UNITS_TO_SECONDS = {
        'm': lambda x: x*60,
        'h': lambda x: x*3600,
        'd': lambda x: x*86400,
        }


class Entry(models.Model):
    """A work done entry"""

    UNIT_CHOICES = (
            ('m', 'minut'),
            ('h', 'godzin'),
            ('d', 'dni'),
            )

    customer = models.ForeignKey(
            'customers.Customer', on_delete=models.PROTECT)
    ticket = models.ForeignKey(
            'tickets.Ticket', on_delete=models.PROTECT,
            null=True, blank=True)
    associate_role = models.ForeignKey(
            'userprofile.AssociateRoleCosts', null=True, blank=True,
            on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    time = models.DecimalField(decimal_places=1, max_digits=6)
    unit = models.CharField(
            max_length=3, choices=UNIT_CHOICES, default='h')
    price = models.DecimalField(decimal_places=2, max_digits=10)

    work_finished_at = models.DateField()
    work_started_at = models.DateField(null=True, blank=True)

    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def duration(self):
        return datetime.timedelta(
                seconds=int(UNITS_TO_SECONDS[self.unit](float(self.time))))

    def duration_hours(self):
        return self.duration().total_seconds()/3600.0

    @property
    def associate(self):
        return self.associate_role.associate if self.associate_role else None

    def calc_cost(self):
        if self.associate_role:
            return decimal.Decimal(str(
                    self.associate_role.manhour_cost))*decimal.Decimal(
                                            str(self.duration_hours()))

    def calc_profit(self):
        if self.associate_role:
            return self.price - self.calc_cost()
