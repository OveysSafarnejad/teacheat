from django.test import TestCase
from django.conf import settings


class TestConfiguration(TestCase):

    def test_security_configuration(self):
        if not settings.DEBUG:
            self.assertTrue(settings.SECURE_SSL_REDIRECT)
            self.assertTrue(settings.SECURE_BROWSER_XSS_FILTER)
            self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF)

    def test_security_in_debug_mode(self):
        self.assertIsNotNone(settings.SECURE_SSL_REDIRECT)
        self.assertIsNotNone(settings.SECURE_BROWSER_XSS_FILTER)
        self.assertIsNotNone(settings.SECURE_CONTENT_TYPE_NOSNIFF)
