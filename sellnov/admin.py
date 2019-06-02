import filesanitize

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

from documents.models import Document


def print_document(request, pk):
    doc = Document.objects.get(pk=pk)
    pdf = doc.as_pdf({'copy': request.GET.get('copy')})
    copy = '_kopia' if request.GET.get('copy') else ''
    filename = filesanitize.safe_path('%s_%s%s.pdf' % (
        doc._meta.verbose_name, doc.number_fmt, copy))
    resp = HttpResponse(content=pdf.read(), content_type='application/pdf')
    resp['Content-Disposition'] = 'filename=%s' % filename
    return resp


class SellnovAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        urls.append(
                path(
                    'documents/<int:pk>/print/',
                    self.admin_view(print_document),
                    name='print_document')
                )
        return urls
