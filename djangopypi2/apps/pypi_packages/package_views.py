from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models.query import Q
from django.http import Http404, HttpResponseRedirect
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from ..pypi_ui.shortcuts import render_to_response
from .decorators import user_maintains_package, user_owns_package
from .models import Package
from .models import Release
from .forms import SimplePackageSearchForm

class Index(ListView):
    model = Package
    context_object_name = 'packages'

class SinglePackageMixin(SingleObjectMixin):
    model = Package
    context_object_name = 'package'
    slug_url_kwarg = 'package_name'
    slug_field = 'name'

class PackageDetails(SinglePackageMixin, DetailView):
    pass

def search(request):
    if request.method == 'POST':
        form = SimplePackageSearchForm(request.POST)
    else:
        form = SimplePackageSearchForm(request.GET)

    if form.is_valid():
        q = form.cleaned_data['query']

    return list_detail.object_list(
        request,
        template_object_name = 'package',
        queryset             = Package.objects.filter(Q(name__contains=q) | 
                                                      Q(releases__package_info__contains=q)).distinct())

class DeletePackage(SinglePackageMixin, DeleteView):
    success_url = reverse_lazy('djangopypi2-packages-index')

    @method_decorator(user_owns_package())
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DeletePackage, self).dispatch(request, *args, **kwargs)
