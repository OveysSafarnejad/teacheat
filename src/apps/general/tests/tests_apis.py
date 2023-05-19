from django.urls import reverse
from rest_framework import status
from apps.core.tests import BaseAPITestCase


class CityApisTests(BaseAPITestCase):

    def tests_cities_list_200(self):
        url = reverse('cities:cities-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
