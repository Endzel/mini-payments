from rest_framework import serializers

from api.models import UserProfile, Account


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class UserAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('user', 'balance',)
