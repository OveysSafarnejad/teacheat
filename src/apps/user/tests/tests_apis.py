import json
from rest_framework import status
from django.urls import reverse

from apps.general.models import City
from apps.core.tests import BaseAPITestCase
from apps.user.models import Address, User


class AddressesApiTests(BaseAPITestCase):

    def setUp(self) -> None:
        user_data = {
            "email": "safarnejad@fakemail.com",
            "password": "supersecret",
        }
        self.user = User.objects.create_user(**user_data)
        self.client.force_authenticate(user=self.user)

        self.city = City(name='city_name')
        self.city.save()

        self.address_data = {
            "title": 'address_title',
            "postal_code": 45676,
            "street": 'street_name',
            "house_number": 1,
            "apt_number": 1,
            "city": self.city,
            "owner": self.user
        }
        Address.objects.create(**self.address_data)
        super().setUp()

    def test_address_creates_successfully_201(self):
        url = reverse('accounts:address-list')
        address_data = {
            "title": "address_title",
            "postal_code": 45676,
            "street": "street_name",
            "house_number": 1,
            "apt_number": 1,
            "city": self.city.id
        }
        response = self.client.post(
            url,
            data=address_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = json.loads(response.content)
        self.assertEqual(response['owner'], self.user.id)

    def test_get_addresses_list_200(self):
        url = reverse('accounts:address-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 1)
