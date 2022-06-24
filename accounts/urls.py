# import patterns as patterns
from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login, name='login'),
    path('forgot/', views.forgot, name='forgot'),
    path('forgot/basarisiz/', views.redirect_active_user, name='redirect_active_user'),
    path('logout/', views.pagelogout, name='view_logout'),
    path('permission/Add', views.show_urls, name='add_permission'),
    path('error/404/', views.handle400Template, name='404'),
    path('error/500/', views.handle500Template, name='500'),
    path(r'referee/', views.referenceReferee, name='referee'),
    path(r'coach/', views.referenceCoach, name='coach'),
    path('pre-registration/', views.pre_registration, name='pre-registration'),
    path('on-kayit/spor-salonu/', views.pre_registration_facility, name='pre_registration_facility'),
    path('on-kayit/sporcu/', views.pre_registration_athelete, name='pre_registration_athelete'),
    path('on-kayit/antrenor/', views.pre_registration_coach_api, name='pre_registration_coach_api'),
    path('on-kayit/basarili/', views.redirect_register, name='redirect_register'),
    path(r'newpassword', views.updateUrlProfile, name='newPassword'),
    path(r'newpassword/basarili/', views.redirect_password_update, name='redirect_password_update'),
    path(r'newpassword/update/', views.redirect_newpassword, name='redirect_newpassword'),
    path('send-newpassword/', views.send_new_password, name='send_new_password'),

]
