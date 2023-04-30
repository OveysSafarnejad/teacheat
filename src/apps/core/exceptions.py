"""
core exceptions module.
"""

from django.utils.encoding import force_str
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException


def _get_error_details(data):
    if isinstance(data, list):
        ret = dict(message=_get_error_details(data[0]))

        return ret
    elif isinstance(data, dict):
        ret = dict()
        for key, value in data.items():
            if not isinstance(value, list) and not isinstance(value, dict):
                value = [value]

            if isinstance(value, dict):
                value = [value.get('message')]

            ret[key] = _get_error_details(value)

        return ret

    return force_str(data)


class ExceptionBase(APIException):
    """
    base class for all application exceptions.
    """
    pass


class BusinessExceptionBase(ExceptionBase):
    """
    base class for all application business exceptions.
    """

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = _('A business error occurred.')


class NotFoundExceptionBase(ExceptionBase):
    """
    base class for all application business exceptions.
    """

    status_code = status.HTTP_404_NOT_FOUND


class InvalidHookTypeError(ExceptionBase):
    """
    invalid hook type error.
    """
    pass


class ValidationError(ExceptionBase):
    """
    validation error.
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'
    default_type = 'field_validation_error'

    def __init__(self, detail=None, code=None, type_=None):
        if detail is None:
            detail = self.default_detail
        if type_ is None:
            type_ = self.default_type

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        result = dict(result=None, type=None)
        result['result'] = _get_error_details(detail)
        result['type'] = type_

        self.detail = result
