from django.conf.urls import patterns, url
from maintenance import views, ajax

urlpatterns = patterns('',
    url(r'^$', views.index, name='maintenance'),
    url(r'^search/$', views.searchWorkshopByCar, name='search_workshop_by_car'),
    url(r'^in_workshop/$', views.inWorkshop, name='in_workshop'),
    url(r'^workshop/list/$', views.workshopList, name='workshop_list'),
    url(r'^workshop/new/$', views.newWorkshop, name='new_workshop'),
    url(r"^workshop/(?P<workshop_id>\d+)/cars/$", views.carsInWorkshop),
    url(r"^workshop/(?P<workshop_id>\d+)/disabled/$", views.onOffWorkshop),
    url(r"^workshop/(?P<workshop_id>\d+)/enabled/$", views.onOffWorkshop),
    url(r'^program/$', views.maintenanceProgram, name='maintenance_program'),
    url(r'^program/form/$', views.maintenanceProgramCar, name='form_maintenance_program'),
    url(r"^program/(?P<mp_id>\d+)/close/$", views.maintenanceProgramClose, name="close_maintenance"),
    url(r"^program/(?P<mp_id>\d+)/open/$", views.maintenanceProgramClose, name="close_maintenance"),
    url(r'^program/search/$', views.searchMaintenanceProgramByCar, name='search_maintenance_program'),
    url(r'^program/ajax_sidebar/$', ajax.lastMaintenance, name='last_maintenance'),
    url(r"^in/workshop/(?P<maintenance_id>\d+)/view/$", views.viewCarInWorkshop, name="view_car_workshop"),
    url(r"^in/workshop/(?P<maintenance_id>\d+)/fixed/$", views.fixedCar, name="fixed_car_workshop"),
)
