
from django.conf.urls import patterns, url
from guest import views, ajax

urlpatterns = patterns('',
    url(r'^$', views.index, name='guest'),
    url(r'^search/$', ajax.searchGuest),
    url(r'^import_guest/', views.importGuest, name='import_guest'),
    url(r'^cleanCI_guest/', views.cleanGuestDocument, name='cleanCI_guest'),
)
