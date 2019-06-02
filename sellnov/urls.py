from django.urls import path
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'sellnov.views.home', name='home'),
    # url(r'^sellnov/', include('sellnov.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    path(r'admin/', admin.site.urls),
    ]
