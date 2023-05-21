import django.contrib.auth.password_validation as validators
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.user.models import Address, User


class UserSignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        label='confirm password',
        write_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password', 'password_confirm',)
        read_only_fields = ('id', 'username',)
        extra_kwargs = {
            'first_name': {
                'required': True,
                'allow_blank': False
            },
            'last_name': {
                'required': True,
                'allow_blank': False
            },
            'password': {
                'write_only': True
            },
            'password_confirm': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        errors = dict()

        try:
            validators.validate_password(password=password)
        except ValidationError as e:
            errors['password'] = list(e.messages)

        if password != password_confirm:
            errors['password'] = _('passwords do not match.')

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSignUpSerializer, self).validate(attrs)

    def create(self, validated_data):
        del validated_data['password_confirm']
        user = User.objects.create_user(**validated_data)
        return user


class UserBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'full_name', )


class UserAddressesSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', required=False)

    class Meta:
        model = Address
        fields = ('id', 'title', 'postal_code', 'city', 'city_name', 'street', 'house_number', 'apt_number', 'owner')
        read_only_fields = ('id', 'city_name', 'owner')

    def create(self, validated_data):
        owner = self.context['request'].user
        address = Address.objects.create(
            owner=owner,
            **validated_data
        )
        return address
