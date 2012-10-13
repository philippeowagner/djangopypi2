import logging
import urlparse
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.static import serve as static_serve
from django.contrib import admin
admin.autodiscover()

log = logging.getLogger(__name__)

def static_urls():
    '''Returns urls for for static file serving from this server. In case
    the STATIC_URL points to an absolute server, we don't serve static
    files from this server.
    '''
    parsed_url = urlparse.urlparse(settings.STATIC_URL)
    if parsed_url.netloc:
        log.debug('Cannot serve STATIC files since settings.STATIC_URL points outside this server.')
        return patterns('')
    return patterns('',
                    url(r'^' + settings.STATIC_URL.strip('/') + r'/(?P<path>.*)$',
                        static_serve, dict(document_root=settings.STATIC_ROOT)))

urlpatterns = patterns('',
    url(r'', include('djangopypi2.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static_urls()
