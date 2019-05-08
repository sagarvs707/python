from django.urls import path
from django.conf.urls import url

from .views import login_view, change_password, logout, register_view, SignupDelete, validate_registration_otp, \
    forgot_password, validate_forgot_password, push_notification

urlpatterns = [
    path('register/', register_view, name='register'),
    path('validate_registration_otp/', validate_registration_otp, name='verify_otp'),

    url(r'^get/(?P<id>[0-9A-Fa-f-]+)/$', SignupDelete.as_view()),
    url(r'^delete/(?P<id>[0-9A-Fa-f-]+)/$', SignupDelete.as_view()),
    url(r'^put/(?P<id>[0-9A-Fa-f-]+)/$', SignupDelete.as_view()),

    path('login/', login_view, name='login'),
    path('change-password/', change_password),
    url(r'^logout/', logout),

    path('forgot_password/', forgot_password),
    path('validate_forgot_password/', validate_forgot_password),

    path('send_notification/', push_notification, name='send_notification'),

]
