from django.conf.urls import patterns, url
from company import views

urlpatterns = patterns('',
    url(r'^new/', views.newCompany, name='new_company'),
)
