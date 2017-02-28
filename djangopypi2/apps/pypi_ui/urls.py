from urlparse import urljoin
from django.conf.urls import include, url
from django.conf import settings
from django.http import HttpResponseRedirect

urlpatterns = [
    url(r'^favicon\.ico$', lambda request: HttpResponseRedirect(urljoin(settings.STATIC_URL, 'favicon.ico'))),
    ]
