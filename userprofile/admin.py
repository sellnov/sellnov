from django.contrib import admin
from .models import (
        BusinessEntity, Role, AssociateRoleCosts, Associate)


@admin.register(BusinessEntity)
class BusinessEntityAdmin(admin.ModelAdmin):
    pass


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'manhour_price')


class AssociateRoleInlineAdmin(admin.TabularInline):
    model = AssociateRoleCosts
    fields = ('role', 'manhour_cost',)


@admin.register(Associate)
class AssociateAdmin(admin.ModelAdmin):
    inlines = [AssociateRoleInlineAdmin]
    list_display = ('name', 'user', 'default_manhour_cost', 'roles_list')
    list_filter = ('roles',)
    search_fields = (
            'name', 'user__email', 'user__first_name', 'user__last_name')

    def roles_list(self, obj):
        return ', '.join(obj.roles.all().values_list('name', flat=True))
    roles_list.short_description = 'roles'
