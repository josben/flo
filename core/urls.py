from django.conf.urls import patterns, url
from core import views

urlpatterns = patterns('',
    url(r'^users/', views.users, name='list_users'),
    url(r"^user/(?P<user_id>\d+)/enabled/$", views.enableDisableUser, name="enabled_user"),
    url(r"^user/(?P<user_id>\d+)/disabled/$", views.enableDisableUser, name="disable_user"),
    url(r"^user/(?P<user_id>\d+)/admin/$", views.isAdminUser, name="is_admin_user"),
    url(r"^user/(?P<user_id>\d+)/change_password/$", views.changePasswordUser, name="change_password_user"),
)
