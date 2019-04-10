from rest_framework import serializers
from viyaan_app.models import Signup


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = ('id', 'first_name', 'last_name', 'email', 'address', 'phone_number', 'password')
