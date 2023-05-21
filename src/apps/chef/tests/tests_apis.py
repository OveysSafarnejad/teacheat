# import json
from django.urls import reverse
from rest_framework import status
from apps.core.tests import BaseAPITestCase
# from apps.chef.tests.schemas import chef_list_schema


class ChefApisTest(BaseAPITestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_getting_chefs_list_200(self):
        url = reverse('chefs:chef-list')
        response = self.client.get(url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response = json.loads(response.content)
        # self.check_response_schema(chef_list_schema, response)
