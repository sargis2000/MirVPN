from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .validators import length_validator
from datetime import datetime
from random import randint
from django.conf import settings


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message='User already registered with this email')]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'],)
        user.set_password(validated_data['password'])
        user.OTP = randint(99999, 999999)
        user.OTP_creation_time = datetime.now()
        user.save()
        return user


class ActivateSerializer(serializers.ModelSerializer):
    OTP = serializers.IntegerField(validators=(length_validator,), required=False)

    class Meta:
        model = User
        fields = ('OTP',)

    def update(self, instance, validated_data):
        if validated_data['OPT']:
            if validated_data['OPT'] != instance.OPT:
                raise serializers.ValidationError({"OPT": 'Wrong One Time Passcode'})
            time = datetime.now() - instance.OPT_creation_time
            if time.total_seconds() > settings.OPT_VALID_TIME:
                instance.OPT = None
                instance.OPT_creation_time = None
                raise serializers.ValidationError({'OPT': 'Passcode Expired'})
            instance.is_active = True
            instance.save()
            return instance

