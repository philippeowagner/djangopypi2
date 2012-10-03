import urlparse
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.static import serve as static_serve

def static_urls():
    '''Returns nothing if we're not in DEBUG, and allows for static
    file serving from this server if the STATIC_URL points to a
    relative location in this server.
    '''
    if not settings.DEBUG:
        return ()
    parsed_url = urlparse.urlparse(settings.STATIC_URL)
    if parsed_url.netloc:
        log.warn('Cannot serve STATIC files since settings.STATIC_URL points outside this server.')
        return ()
    return patterns('',
                    url(r'^' + settings.STATIC_URL.strip('/') + r'/(?P<path>.*)$',
                        static_serve, dict(document_root=settings.STATIC_ROOT)))

urlpatterns = patterns('',
    url(r'', include('djangopypi2.apps.pypi_ui.urls')),
    url(r'', include('djangopypi2.apps.pypi_frontend.urls')),
) + static_urls()
