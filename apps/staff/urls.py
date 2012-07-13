from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf.urls.static import static
#import settings, os

urlpatterns = patterns("",
    url(r"^$", "flo.apps.staff.views.staff", name="staff"),
    url(r"^form/", "flo.apps.staff.views.register", name="register"),
    url(r"^(?P<staff_id>\d+)/driver/$", "flo.apps.staff.views.register_driver", name="driver"),
    url(r"^unit/", "flo.apps.staff.views.create_unit", name="create_unit"),
    url(r"^role/", "flo.apps.staff.views.create_role", name="create_role"),
    url(r"^list/", "flo.apps.staff.views.listing", name="listing"),
#    url(r'^media/(?P<path>.*)$', "django.views.static.serve", {'document_root': os.path.join(settings.MEDIA_ROOT, 'site_media')}),
    #url(r"^$", direct_to_template, {"template": "staff/register.html"}, name="register"),
) #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
import os
urlpatterns += patterns('',
        (r'^site_media/media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'site_media/media')}),
)
"""
"""
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
"""
