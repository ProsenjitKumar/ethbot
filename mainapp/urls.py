from django.urls import re_path
from .views import *
from django.contrib.auth import views as auth_views #import this

urlpatterns = [
    re_path('^$', index, name='index'),
    re_path('dashboard/', dashboard, name='dashboard'),
    re_path('signin/', login_view, name='signin'),
    re_path('logout/', user_logout, name='logout'),
    re_path('kyc/', kyc_view, name='kyc'),
    re_path('profile/', profile_view, name='profile'),
    re_path('refer/', refer, name='refer'),
    re_path("password_reset", password_reset_request, name="password_reset"),
    re_path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='index/reset/password_reset_done.html'),
         name='password_reset_done'),
    re_path('reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/',
         auth_views.PasswordResetConfirmView.as_view(template_name="index/reset/password_reset_confirm.html"),
         name='password_reset_confirm'),
    re_path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='index/reset/password_reset_complete.html'),
         name='password_reset_complete'),
    # re_path('otp/', otp_view, name='otp')
    re_path('activate/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/',
        activate, name='activate'),

]