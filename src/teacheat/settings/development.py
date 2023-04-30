from teacheat.settings.base import *

# local database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

# Add SQL statement logging in development
if os.environ.get('SQL_DEBUG', default="0") == 'true':
    LOGGING['loggers']['django.db'] = {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False
    }


# Disable caching while in development
CACHES = {
    'default': {
        'BACKEND': os.environ.get('CACHE_BACKEND', 'django.core.cache.backends.dummy.DummyCache')
    }
}


# set up Django Debug Toolbar if installed
try:
    import debug_toolbar  # noqa

    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INSTALLED_APPS.append('debug_toolbar')
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': 'debug_toolbar.middleware.show_toolbar',
    }
except ImportError:
    print('Could not import "debug_toolbar" package.')
