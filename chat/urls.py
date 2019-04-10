from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('chats', views.ChatView)



urlpatterns = [
    # URL form : "/api/messages/1/2"
    path('messages_get/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),  # For GET request.
    # URL form : "/api/messages/"
    path('messages_post/', views.message_list, name='message-list'),   # For POST
    # URL form "/api/users/1"
    path('users_get/<int:pk>', views.user_list, name='user-detail'),      # GET request for user with id
    path('users/', views.user_list, name='user-list'),    # POST for new user and GET for all users list


    path('chat', include(router.urls))
]