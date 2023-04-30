"""
WSGI config for teacheat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
from os.path import basename, dirname


settings_package = basename(dirname(__file__)) + '.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_package)
application = get_wsgi_application()
