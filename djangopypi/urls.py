# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from djangopypi.feeds import ReleaseFeed
from djangopypi.views import root as root_views
from djangopypi.views import packages as packages_views
from djangopypi.views import releases as releases_views

PACKAGE = r'(?P<package>[\w\d_\.\-]+)'
VERSION = r'(?P<version>[\w\d_\.\-]+)'

urlpatterns = patterns('',
    url('^$', root_views.root, name="djangopypi-root"),

    url('^packages/$', packages_views.index, name='djangopypi-package-index'),
    url('^simple/$', packages_views.simple_index, name='djangopypi-package-index-simple'),
    url('^search/$', packages_views.search,name='djangopypi-search'),
    url('^rss/$', ReleaseFeed(), name='djangopypi-rss'),
    
    url('^simple/' + PACKAGE + '/$', packages_views.simple_details,
        name='djangopypi-package-simple'),
    
    url('^pypi/$', root_views.root, name='djangopypi-release-index'),
    url('^pypi/' + PACKAGE + '/$', packages_views.details,
        name='djangopypi-package'),
    url('^pypi/' + PACKAGE + '/rss/$', ReleaseFeed(),
        name='djangopypi-package-rss'),    
    url('^pypi/' + PACKAGE + r'/doap\.rdf$', packages_views.doap,
        name='djangopypi-package-doap'),
    url('^pypi/' + PACKAGE + '/manage/$', packages_views.manage,
        name='djangopypi-package-manage'),
    url('^pypi/' + PACKAGE + '/manage/versions/$', packages_views.manage_versions,
        name='djangopypi-package-manage-versions'),
    
    url('^pypi/' + PACKAGE + '/' + VERSION + '/$',
        releases_views.details, name='djangopypi-release'),
    url('^pypi/' + PACKAGE + '/' + VERSION + r'/doap\.rdf$',
        releases_views.doap, name='djangopypi-release-doap'),
    url('^pypi/' + PACKAGE + '/' + VERSION + '/manage/$',
        releases_views.manage, name='djangopypi-release-manage'),
    url('^pypi/' + PACKAGE + '/' + VERSION + '/metadata/$',
        releases_views.manage_metadata, name='djangopypi-release-manage-metadata'),
    url('^pypi/' + PACKAGE + '/' + VERSION + '/files/$',
        releases_views.manage_files, name='djangopypi-release-manage-files'),
    url('^pypi/' + PACKAGE + '/' + VERSION + '/files/upload/$',
        releases_views.upload_file, name='djangopypi-release-upload-file'),
)
