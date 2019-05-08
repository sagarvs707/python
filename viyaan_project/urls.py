from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from viyaan_app.views import push_notification

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('viyaan_app.urls')),
    path('course/', include('courses.urls')),

    path('send_notification/', push_notification, name='send_notification'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)