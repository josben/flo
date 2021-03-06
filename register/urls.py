
from django.conf.urls import patterns, url
from register import views, ajax

urlpatterns = patterns('',
    url(r'^$', views.index, name='register'),
    url(r'^guest_form/', views.registerGuest, name='guest_form'),
    url(r'^guests/today/', views.listGuestsToday, name='list_today_guests'),
    url(r'^guests/withoutexit/', views.listGuestsWithoutExit, name='list_guests_without_exit'),
    url(r'^guests/', views.list_guests, name='list_guests'),
    url(r"^guest/(?P<register_id>\d+)/stop/$", views.stop_guest, name="stop_guest"),
    url(r"^(?P<register_id>\d+)/edit/$", views.editRegisterCar, name="edit_register_car"),
    url(r"^(?P<register_id>\d+)/detail/$", views.detailRegisterCar, name="detail_register_car"),
    url(r"^(?P<register_id>\d+)/view/both/$", views.viewCompleteRegisterCar, name="view_complete_register_car"),
    url(r"^(?P<register_id>\d+)/view/$", views.viewRegisterCar, name="view_register_car"),
    url(r"^(?P<register_id>\d+)/select/workshop/$", views.selectByRegisterWorkshop, name="register_select_workshop"),
    url(r"^search/car/$", views.searchByCar, name="search_by_car"),
    url(r"^search/driver/$", views.searchByDriver, name="search_by_driver"),
    url(r"^search/ladder/$", views.searchByLadder, name="search_by_ladder"),
    url(r"^search/event/car/$", views.searchByCarAndEvent, name="search_by_car_event"),
    url(r"^search/event/driver/$", views.searchByDriverAndEvent, name="search_by_driver_event"),
    url(r"^search/event/ladder/$", views.searchByLadderAndEvent, name="search_by_ladder_event"),
    url(r"^search/guest/$", views.searchByGuest, name="search_by_guest"),
    url(r"^search/guest_ci/$", views.searchByCI, name="search_by_guest_ci"),
#    url(r'^edit/(?P<pk>\d+)/$', views.CarRegistrationUpdate.as_view(), name='car_registration_edit'),
    url(r'^register_form/', views.registerCar, name='form_register_car'),
    url(r'^foreign_register_form/', views.registerForeignCar, name='form_foreign_register_car'),
    url(r'^last/cars/', views.lastRegisters, name='last_registers'),
    url(r'^registers_day/', views.registers_day, name='registers_day'),
    url(r'^registers_all/', views.registers_all, name='registers_all'),
    url(r'^registers_input/', views.registersInput, name='registers_input'),
    url(r'^registers_output/', views.registersOutput, name='registers_output'),
    url(r'^registers_both/', views.registersBoth, name='registers_both'),
    url(r'^mregister_form/', views.registerSimplifiedCar, name='form_register_simplified_car'),
    # Ajax Functions
    url(r'^ajax_validation_car/', ajax.validation_car, name='ajax_validation_car'),
    url(r'^ajax_sidebar/', ajax.validation_car_sidebar, name='ajax_sidebar'),
    url(r'^ajax_delete_date_session/', ajax.delete_date_session, name='ajax_delete_date_session'),
)
