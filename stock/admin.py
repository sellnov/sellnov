"""
This is a module docstring
"""

__author__ = "Marcin Nowak"
__copyright__ = "Copyright 2013"
__license__ = "Propertiary"
__maintainer__ = "Marcin Nowak"
__email__ = "marcin.j.nowak@gmail.com"


from django.contrib import admin
from models import Product, Tax, Unit

admin.site.register(Product)
admin.site.register(Tax)
admin.site.register(Unit)
