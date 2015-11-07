from django.conf.urls import patterns, url
from notifications import views, ajax

urlpatterns = patterns('',
    url(r'^$', views.notifications, name='notifications'),
    url(r'^my/notifications/$', views.myNotifications, name='my_notifications'),
    url(r'^admin/new/$', views.createNotificationFromAdmin, name='new_notification_admin'),
    url(r'^new/$', views.createNotification, name='new_notification'),
    url(r"^(?P<notification_id>\d+)/view/$", ajax.viewNotification),
)
