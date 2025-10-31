from django.contrib import admin

from .models import AutoNumber


@admin.register(AutoNumber)
class AutoNumberAdmin(admin.ModelAdmin):
    list_display = (
        "document_type",
        "last_number",
        "last_date",
        "reset_by",
        "business_entity",
    )
