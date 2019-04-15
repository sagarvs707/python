from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import url


from .views import login_view, change_password, logout, register_view, SignupDelete, validate_registration_otp, forgot_password, validate_forgot_password, image_upload, model_form_upload

urlpatterns = [
    path('register/', register_view, name='register'),
    path('validate_registration_otp', validate_registration_otp, name='verify_otp'),


    url(r'^get/(?P<id>[0-9A-Fa-f-]+)/$', SignupDelete.as_view()),
    url(r'^delete/(?P<id>[0-9A-Fa-f-]+)/$', SignupDelete.as_view()),
    url(r'^put/(?P<id>[0-9A-Fa-f-]+)/$', SignupDelete.as_view()),

    path('login/', login_view, name='login'),
    path('change-password/', change_password),
    url(r'^logout/', logout),

    path('forgot_password/', forgot_password),
    path('validate_forgot_password/', validate_forgot_password),

    url(r'^uploads/image/$', image_upload, name='picture'),
    url(r'^uploads/form/image/$', model_form_upload, name='picture'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)