"""
This is a module docstring
"""

__author__ = "Marcin Nowak"
__copyright__ = "Copyright 2013"
__license__ = "Propertiary"
__maintainer__ = "Marcin Nowak"
__email__ = "marcin.j.nowak@gmail.com"


from django.template.loader import render_to_string
from django.conf import settings
from z3c.rml import rml2pdf


def create_pdf(obj, template_name, extra_context=None):
    ctx = extra_context or {}
    ctx.update({
            'object': obj,
            'fontdir': settings.FONT_DIR,
            })
    rml = render_to_string(template_name, ctx)
    return rml2pdf.parseString(rml)


