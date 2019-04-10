from django.contrib.auth.models import User
from viyaan_app.models import Signup
from rest_framework import serializers
from chat.models import Message
#
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    """For Serializing User"""
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Signup
        fields = ['email', 'password']
#
# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    """For Serializing Message"""
    sender = serializers.SlugRelatedField(many=False, slug_field='email', queryset=Signup.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='email', queryset=Signup.objects.all())
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']