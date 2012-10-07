from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from . import xmlrpc_views
from . import distutils_request

@csrf_exempt
def root(request):
    """ Root view of the package index, handle incoming actions from distutils
    or redirect to a more user friendly view """
    if xmlrpc_views.is_xmlrpc_request(request):
        return xmlrpc_views.handle_xmlrpc_request(request)

    if distutils_request.is_distutils_request(request):
        return distutils_request.handle_distutils_request(request)

    return HttpResponseRedirect(reverse('djangopypi2-package-index'))
