# coding: utf-8

from django.conf import settings
from django.db import models

import arrow
import pglock


def format_number(document_class, number, date):
    fmt = document_class.AUTONUMBER_FORMAT
    ctx = {
            'number': number,
            'year': date.year,
            'month': date.month,
            'day': date.day,
            }
    return fmt % ctx


class AutoNumberManager(models.Manager):
    def recalculate_max_number(self, business_entity, document_class):
        doctype = document_class.document_type_name()

        try:
            doc = document_class.objects.filter(
                selected_owner=business_entity,
                doctype=doctype
            ).order_by('-issue_date', '-number')[0]
        except IndexError:
            self.model.objects.filter(
                business_entity=business_entity,
                document_type=doctype).delete()
        else:
            try:
                an = self.model.objects.get(
                    business_entity=business_entity, document_type=doctype)
            except self.model.DoesNotExist:
                pass
            else:
                an.last_number = doc.number
                an.last_date = doc.issue_date
                an.save()

    def acquire(self, business_entity, document_class, date=None):
        document_type = document_class.document_type_name()
        if not date:
            date = arrow.now(settings.TIME_ZONE).date()
        pglock.acquire_lock(self.model)
        try:
            an = self.get_queryset().get(
                business_entity=business_entity,
                document_type=document_type)
        except AutoNumber.DoesNotExist:
            self.create(
                    business_entity=business_entity,
                    document_type=document_type,
                    last_number=1, last_date=date)
            number = 1
        else:
            if an.reset_by == 'month':
                if (an.last_date.month == date.month
                        and an.last_date.year == date.year):
                    number = an.last_number+1
                else:
                    number = 1
            elif an.reset_by == 'year':
                if an.last_date.year == date.year:
                    number = an.last_number+1
                else:
                    number = 1
            an.last_number = number
            an.last_date = date
            an.save()
        return number


class AutoNumber(models.Model):
    document_type = models.CharField(max_length=64)
    last_number = models.IntegerField()
    last_date = models.DateField()
    business_entity = models.ForeignKey(
        'userprofile.BusinessEntity', on_delete=models.CASCADE)
    reset_by = models.CharField(max_length=16, choices=(
        ('month', u'co miesiąc'),
        ('year', u'co rok'),
        ), default='year')

    objects = AutoNumberManager()

    class Meta:
        unique_together = ('document_type', 'business_entity')
