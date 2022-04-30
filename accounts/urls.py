# import patterns as patterns
from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login, name='login'),
    path('forgot/', views.forgot, name='view_forgot'),
    path('logout/', views.pagelogout, name='view_logout'),
    path('permission/Add', views.show_urls, name='add_permission'),
    path('error/404/', views.handle400Template, name='404'),
    path('error/500/', views.handle500Template, name='500'),
    path(r'referee/', views.referenceReferee, name='referee'),
    path(r'coach/', views.referenceCoach, name='coach'),
    path('pre-registration/', views.pre_registration, name='pre-registration'),
    path('on-kayıt/spor-salonu', views.pre_registration_facility, name='pre_registration_facility'),

]
