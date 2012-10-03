from django.conf import settings
from django.contrib import admin
from .models import *

admin.site.register(Package)
admin.site.register(Release)
admin.site.register(Distribution)
admin.site.register(Review)

if getattr(settings,'DJANGOPYPI_MIRRORING', False):
    admin.site.register(MasterIndex)
    admin.site.register(MirrorLog)
