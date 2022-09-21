from rest_framework import serializers
from profiles_api import models


class MessageSerializer(serializers.Serializer):
    """Serializes a message"""
    username = serializers.CharField(max_length=255)
    message = serializers.CharField(max_length=1024)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create a new user"""
        user = models.UserProfile.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)
