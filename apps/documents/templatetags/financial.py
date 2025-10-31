"""
This is a module docstring
"""

__author__ = "Marcin Nowak"
__copyright__ = "Copyright 2013"
__license__ = "Propertiary"
__maintainer__ = "Marcin Nowak"
__email__ = "marcin.j.nowak@gmail.com"


import sellnov.utils
from django import template

register = template.Library()


@register.filter
def as_words(value):
    return sellnov.utils.value_as_words(abs(value))
