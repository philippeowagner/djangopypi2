from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^manage/$', views.index, name='djangopypi2-manage'),
    ]
