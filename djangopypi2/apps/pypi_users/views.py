from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

def index(request):
    return render_to_response('pypi_users/index.html', context_instance=RequestContext(request))

@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render_to_response('pypi_users/user_profile.html', dict(user=user), context_instance=RequestContext(request))
