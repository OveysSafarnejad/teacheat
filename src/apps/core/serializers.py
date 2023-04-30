# -*- coding: utf-8 -*-
"""
core serializers module.
"""

from collections import OrderedDict
from collections.abc import Mapping

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.fields import empty, get_error_detail, set_value, SkipField
from rest_framework.serializers import as_serializer_error, ModelSerializer, Serializer
from rest_framework.settings import api_settings


from apps.core.exceptions import ValidationError


class CoreSerializer(Serializer):
    """
    core serializer class.

    every serializer class must be subclassed from this class.
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'permissions'):
            if self.user is None and self.context is not None:
                try:
                    user = self.context['request'].user
                    if user is not None and user.has_employee:
                        self.user = user.employee
                except KeyError:
                    pass

    def to_representation(self, instance):
        represented_data = super().to_representation(instance)
        if self.user is not None:
            try:
                permissions = self.Meta.permissions.items()
                # for field, permission in permissions:
                #     if not security_services.has_permission(self.user, *permission):
                #         represented_data[field] = None
            except AttributeError:
                ...
                # sentry_sdk.capture_message(
                #     'Class {serializer_class} missing "Meta.permissions" attribute'.format(
                #         serializer_class=self.__class__.__name__)
                # )
        return represented_data

    def to_internal_value(self, data):
        """
        Dict of native values <- Dict of primitive datatypes.
        """
        if not isinstance(data, Mapping):
            message = self.error_messages['invalid'].format(
                datatype=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='invalid')

        ret = OrderedDict()
        errors = OrderedDict()
        fields = self._writable_fields

        for field in fields:
            validate_method = getattr(self, 'validate_' + field.field_name, None)
            primitive_value = field.get_value(data)
            try:
                validated_value = field.run_validation(primitive_value)
                if validate_method is not None:
                    validated_value = validate_method(validated_value)
            except RestValidationError as exc:
                errors[field.field_name] = exc.detail
            except DjangoValidationError as exc:
                errors[field.field_name] = get_error_detail(exc)
            except SkipField:
                pass
            else:
                set_value(ret, field.source_attrs, validated_value)

        if errors:
            raise ValidationError(errors)

        return ret

    def run_validation(self, data=empty):
        """
        We override the default `run_validation`, because the validation
        performed by validators and the `.validate()` method should
        be coerced into an error dictionary with a 'non_fields_error' key.
        """
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        value = self.to_internal_value(data)
        try:
            self.run_validators(value)
            value = self.validate(value)
            assert value is not None, '.validate() should return the validated data'
        except (RestValidationError, DjangoValidationError) as exc:
            raise ValidationError(detail=as_serializer_error(exc))

        return value


class CoreModelSerializer(ModelSerializer, CoreSerializer):
    """
    core model serializer class.

    every serializer need to have permission feature in
    representation state must be subclassed from this.
    """
    pass
