from django.db import models
from django.utils.translation import ugettext_lazy as _

class GlobalConfigurationManager(models.Manager):
    def latest(self):
        try:
            return super(GlobalConfigurationManager, self).latest()
        except GlobalConfiguration.DoesNotExist:
            global_configuration = GlobalConfiguration()
            global_configuration.save()
            return global_configuration

class GlobalConfiguration(models.Model):
    '''Stores the configuration of this site. As a rule, the most
    recent configuration is always used, and past configurations
    are kept for reference and for rollback.
    '''
    objects = GlobalConfigurationManager()

    timestamp = models.DateTimeField(auto_now_add=True)
    allow_version_overwrite = models.BooleanField(default=False)
    upload_directory = models.CharField(max_length=256, default='dists',
        help_text='Direcory relative to MEDIA_ROOT in which user uploads are kept')

    class Meta:
        ordering = ('-timestamp', )
        verbose_name = _(u'global configuration')
        verbose_name_plural = _(u'global configurations')
        get_latest_by = 'timestamp'

class MirrorSite(models.Model):
    enabled = models.BooleanField(default=False)
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class MirrorLog(models.Model):
    mirror_site = models.ForeignKey(MirrorSite, related_name='logs')
    created = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=256)
    
    def __unicode__(self):
        return self.action
    
    class Meta:
        get_latest_by = 'created'
