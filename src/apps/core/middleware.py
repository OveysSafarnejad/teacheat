# -*- coding: utf-8 -*-
"""
core middleware module.
"""

from django.utils import translation


class ForceEnglishAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin'):
            translation.activate('en')
            request.LANGUAGE_CODE = 'en'
        else:
            translation.activate('fa-IR')
            request.LANGUAGE_CODE = 'fa-IR'

        return self.get_response(request)
