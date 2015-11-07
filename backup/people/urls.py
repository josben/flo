from django.conf.urls import patterns, include, url
from people import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^upload_staff', views.uploadStaff, name='upload_staff'),
    url(r'^upload_driver', views.uploadDriver, name='upload_driver'),
)
