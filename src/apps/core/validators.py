# -*- coding: utf-8 -*-
"""
core validators module.
"""

import re

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

PHONE_REGEX = re.compile(r'^0\d{10}$')
MOBILE_REGEX = re.compile(r'^09\d{9}$')
NATIONAL_CODE_REGEX = re.compile(r'^\d{10}$')
IBAN_REGEX = re.compile(r'^IR\d{24}$')
CARD_NUMBER_REGEX = re.compile(r'^[^0]\d{15}$')


def is_valid_mobile(mobile):
    """
    gets a value indicating that given mobile number is valid.

    :param str mobile: mobile number.

    :rtype: bool
    """

    if mobile in (None, '') or not MOBILE_REGEX.match(mobile):
        return False

    return True


def validate_mobile(mobile):
    """
    validates given mobile number.

    :param str mobile: mobile number.

    :raises ValidationError: validation error.
    """

    if not is_valid_mobile(mobile):
        raise ValidationError(_('Provided mobile number is invalid.'))


def is_valid_national_code(code):
    """
    gets a value indicating that given code is a valid national code.

    :param str code: national code.

    :rtype: bool
    """

    if code in (None, '') or not re.search(NATIONAL_CODE_REGEX, code):
        return False

    check_sum = int(code[9])
    total = sum([int(code[x]) * (10 - x) for x in range(9)]) % 11
    return (2 > total == check_sum) or (total >= 2 and check_sum + total == 11)


def validate_national_code(code):
    """
    validates that given code is a valid national code.

    :param str code: national code.

    :raises ValidationError: validation error.
    """

    if not is_valid_national_code(code):
        raise ValidationError(_('Provided national code is invalid.'))


def is_valid_phone(phone):
    """
    gets a value indicating that given phone number is valid.

    :param str phone: phone number.

    :keyword str field_name: field name.

    :rtype: bool
    """

    if phone in (None, '') or not PHONE_REGEX.match(phone):
        return False

    return True


def validate_phone(phone, **options):
    """
    validates given phone number.

    :param str phone: phone number.

    :keyword str field_name: field name.

    :raises ValidationError: validation error.
    """

    field_name = options.get('field_name', 'message')
    if not is_valid_phone(phone):
        raise ValidationError({
            field_name: _('Provided phone number is invalid.')
        })


def is_valid_iban(iban):
    """
    gets a value indicating that given iban is valid.

    :param str iban: iban.

    :rtype: bool
    """

    if iban in (None, '') or not IBAN_REGEX.match(iban):
        return False

    return True


def validate_iban(iban, **options):
    """
    validates given iban.

    :param str iban: iban.

    :keyword str field_name: field name.

    :raises ValidationError: validation error.
    """

    field_name = options.get('field_name', 'message')
    if not is_valid_iban(iban):
        raise ValidationError({
            field_name: _('Provided iban is invalid.')
        })


def is_valid_card_number(card_number):
    """
    gets a value indicating that given card number is valid.

    :param str card_number: card number.

    :rtype: bool
    """

    if card_number in (None, '') or not CARD_NUMBER_REGEX.match(card_number):
        return False

    return True


def validate_card_number(card_number, **options):
    """
    validates given card number.

    :param str card_number: card number.

    :keyword str field_name: field name.

    :raises ValidationError: validation error.
    """

    field_name = options.get('field_name', 'message')
    if not is_valid_card_number(card_number):
        raise ValidationError({
            field_name: _('Provided card number is invalid.')
        })
