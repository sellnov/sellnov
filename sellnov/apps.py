from django.contrib.admin.apps import AdminConfig


class SellnovConfig(AdminConfig):
    default_site = 'sellnov.admin.SellnovAdminSite'
