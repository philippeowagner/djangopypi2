from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db.models.query import Q
from django.forms.models import inlineformset_factory
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView

from ..pypi_metadata.models import Classifier
from ..pypi_ui.shortcuts import render_to_response

from .decorators import user_maintains_package, user_owns_package
from .models import Package, Release
from .forms import SimplePackageSearchForm, AdvancedPackageSearchForm

class Index(ListView):
    model = Package
    context_object_name = 'packages'

    def get_queryset(self):
        if 'query' in self.request.GET:
            q = self.request.GET['query']
            results = Package.objects.filter(Q(name__icontains=q) | Q(releases__package_info__contains=q)).distinct()
            return results
        return Package.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['search_form'] = SimplePackageSearchForm(self.request.GET)
        return context

def advanced_search(request):
    if request.method == 'POST':
        form = AdvancedPackageSearchForm(request.POST)
        if form.is_valid():
            qname = form.cleaned_data['name']
            qsummary = form.cleaned_data['summary']
            qdescription = form.cleaned_data['description']
            qclassifier = set(unicode(x) for x in form.cleaned_data['classifier'])
            qkeyword = set(x.lower() for x in form.cleaned_data['keywords'].split())

            qset = Package.objects.all()
            if qname:
                qset = qset.filter(name__icontains = qname)
            evaled = False
            if qsummary:
                if not evaled:
                    qset = list(qset)
                evaled = True
                qset = filter(lambda x: all(y in x.latest.summary.lower() for y in qsummary.lower().split()), qset)
            if qdescription:
                if not evaled:
                    qset = list(qset)
                evaled = True
                qset = filter(lambda x: all(y in x.latest.description.lower() for y in qdescription.lower().split()), qset)
            if qclassifier:
                if not evaled:
                    qset = list(qset)
                evaled = True
                qset = filter(lambda x: set(x.latest.classifiers) & qclassifier == qclassifier, qset)
            if qkeyword:
                if not evaled:
                    qset = list(qset)
                evaled = True
                qset = filter(lambda x: set(y.lower() for y in x.latest.keywords) & qkeyword == qkeyword, qset)

            if not evaled:
                result = list(qset)
            else:
                result = qset
    else:
        form = AdvancedPackageSearchForm()
        result = None
    return render(request, 'pypi_packages/package_search.html', {
        'search_form': form,
        'search_result': result
    })

class SinglePackageMixin(SingleObjectMixin):
    model = Package
    context_object_name = 'package'
    slug_url_kwarg = 'package_name'
    slug_field = 'name'

class PackageDetails(SinglePackageMixin, DetailView):
    pass

class PackagePermission(SinglePackageMixin, UpdateView):
    template_name = 'pypi_packages/package_permission.html'

    def post(self, request, *args, **kwargs):
        package = self.get_object()
        if request.user not in package.owners.all():
            return HttpResponseForbidden()

        user = get_object_or_404(User, username__exact = self.request.POST['username'])
        action = self.request.POST['action']
        relation = self.request.POST['relation']
        if action == 'add':
            if relation == 'owner':
                package.owners.add(user)
            elif relation == 'maintainer':
                package.maintainers.add(user)
        elif action == 'delete':
            if relation == 'owner':
                if package.owners.count() == 1:
                    return HttpResponseForbidden()
                package.owners.remove(user)
            elif relation == 'maintainer':
                package.maintainers.remove(user)
        return HttpResponse()

class DeletePackage(SinglePackageMixin, DeleteView):
    success_url = reverse_lazy('djangopypi2-packages-index')

    @method_decorator(user_owns_package())
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DeletePackage, self).dispatch(request, *args, **kwargs)
