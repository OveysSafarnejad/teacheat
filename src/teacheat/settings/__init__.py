"""
    Base config loader

    It will try to find development config for the project, otherwise
    it will use production environment settings.
"""


try:
    from teacheat.settings.development import * # noqa
except ImportError:
    from teacheat.settings.production import * # noqa
