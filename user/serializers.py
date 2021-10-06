from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User(**validated_data)

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        return instance

    class Meta:
        model = User
        fields = ('id', 'social_type', 'nickname')