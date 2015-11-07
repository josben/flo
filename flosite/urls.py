from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from flosite import views
#from userena import views as userena_views
#from userena import settings as userena_settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
#    url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    url(r'^$', views.index, name="home"),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name="about"),
    url(r'^accounts/', include('userena.urls')),
    url(r'^messages/', include('userena.contrib.umessages.urls')),
    url(r'^staff/', include('staff.urls')),
    url(r'^branchoffice/', include('branchoffice.urls')),
    url(r'^register/', include('register.urls')),
    url(r'^guest/', include('guest.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^maintenance/', include('maintenance.urls')),
    url(r'^company/', include('company.urls')),
    url(r'^notifications/', include('notifications.urls')),
    url(r'^report/', include('report.urls')),

    # Examples:
    # url(r'^$', 'flosite.views.home', name='home'),
    # url(r'^flosite/', include('flosite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

