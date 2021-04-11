from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ToDo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
