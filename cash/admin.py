from django.contrib import admin
from django.utils.translation import ugettext as _
from models import Account, Operation, Transfer, TransferWithBalance, MonthlyTransferBalance
import calendar


class TransferInlineAdmin(admin.TabularInline):
    model = Transfer
    max_num = 2
    extra = 2


class OperationAdmin(admin.ModelAdmin):
    list_display = ('title', 'estimated_amount', 'date', 'done')
    list_filter = ('draft', 'date')
    ordering = ('date', '-created')
    inlines = (TransferInlineAdmin,)

    def done(self, instance):
        return not instance.draft
    done.boolean = True


class TransferAdmin(admin.ModelAdmin):
    list_display = ('title', 'account', 'amount', 'balance', 'date', 'done')
    list_filter = ('account', 'operation__draft',)
    ordering = ('operation__date', '-operation__created', 'amount')

    def done(self, instance):
        return not instance.operation.draft
    done.boolean = True

    def title(self, instance):
        return u'<a href="../operation/%s">%s</a>' % (instance.operation.pk, instance.operation.title)
    title.allow_tags = True

    def estimated_amount(self, instance):
        return instance.operation.estimated_amount

    def date(self, instance):
        return instance.operation.date

    def has_add_permission(self, *args, **kw):
        return False

    def has_delete_permission(self, *args, **kw):
        return False


class MonthlyTransferBalanceAdmin(admin.ModelAdmin):
    list_display = ('month_name', 'account_name', 'sum_amount', 'balance',)
    list_filter = ('account', 'year', 'month' )
    ordering = ('year', 'month', 'account')

    def account_name(self, instance):
        return instance.account.name

    def has_add_permission(self, *args, **kw):
        return False

    def has_delete_permission(self, *args, **kw):
        return False

    def month_name(self, instance):
        return u'<a href="../operation/?date__year=%s&date__month=%s">%s %s</a>' % (
            instance.year, instance.month, instance.year, _(calendar.month_name[instance.month]))
    month_name.allow_tags = True


admin.site.register(Account)
admin.site.register(Operation, OperationAdmin)
admin.site.register(TransferWithBalance, TransferAdmin)
admin.site.register(MonthlyTransferBalance, MonthlyTransferBalanceAdmin)
