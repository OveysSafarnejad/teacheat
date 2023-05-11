import django.contrib.auth.password_validation as validators
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.user.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        label='confirm passowrd',
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