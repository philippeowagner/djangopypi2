import pytz
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django import forms
from django.conf import settings
from crispy_forms.helper import FormHelper
from ..pypi_ui.shortcuts import render_to_response
from ...website import user_settings

def _administrator_required(func):
    @login_required
    def _decorator(request, *args, **kwargs):
        if not request.user.is_staff:
            return render_to_response('pypi_manage/forbidden.html', context_instance=RequestContext(request))
        return func(request, *args, **kwargs)
    return _decorator

def _get_website_settings_form(*args, **kwargs):
    class WebsiteSettingsForm(forms.Form):
        def __init__(self, *args, **kwargs):
            self.helper = FormHelper()
            self.helper.form_style = 'inline'
            self.helper.help_text_inline = True
            super(WebsiteSettingsForm, self).__init__(*args, **kwargs)

        for available_setting in user_settings.AVAILABLE_SETTINGS:
            name = available_setting['name']
            initial = settings.USER_SETTINGS[name]
            if available_setting['type'] == 'timezone':
                exec '''{} = forms.ChoiceField(choices={!r}, initial={!r})'''.format(
                    name, tuple((x, x) for x in pytz.all_timezones), initial)
            elif available_setting['type'] == 'bool':
                exec '''{} = forms.ChoiceField(choices=((True, "On"), (False, "Off")), initial=("On" if {!r} else "Off"))'''.format(name, initial)
            elif available_setting['type'] == 'names_and_emails':
                exec '''{} = forms.EmailField(initial={!r}, help_text='Email address to send error reports to')'''.format(name, '' if not initial else initial[1])
            else:
                exec '''{} = forms.CharField(initial={!r})'''.format(name, initial)
    return WebsiteSettingsForm(*args, **kwargs)

@_administrator_required
def index(request):
    if request.method == 'POST':
        website_settings_form = _get_website_settings_form(request.POST)
    else:
        website_settings_form = _get_website_settings_form()
    return render_to_response('pypi_manage/index.html', context_instance=RequestContext(request, locals()))
