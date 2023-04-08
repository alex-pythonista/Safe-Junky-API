from rest_framework import serializers
from . import models


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('email', 'phone_number', 'full_name', 'password')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = models.User.objects.create_user(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class VerifyOtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('email', 'phone_number', 'full_name')



class EmergencyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmergencyInformation
        fields = [
            'blood_group',
        ]

    def create(self, validated_data):
        emergency_info = models.EmergencyInformation.objects.create(
            user=self.context['request'].user,
            blood_group=validated_data['blood_group'],
        )
        return emergency_info
    
class ContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContactInformation
        fields = [
            'id',
            'user',
            'name',
            'phone_number',
        ]