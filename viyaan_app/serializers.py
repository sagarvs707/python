from rest_framework import serializers
from viyaan_app.models import Signup


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = ('id', 'full_name', 'email', 'phone_number', 'password', 'profile_picture')
