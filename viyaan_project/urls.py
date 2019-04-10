from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('viyaan_app.urls')),
    path('account/', include('viyaan_app.urls')),
    path('api/', include('chat.urls')),

]
