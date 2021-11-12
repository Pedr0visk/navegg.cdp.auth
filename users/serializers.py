from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserImpersonationSerializer(serializers.Serializer):
    token = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    expire_at = serializers.DateTimeField(read_only=True)


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'acc_id')
