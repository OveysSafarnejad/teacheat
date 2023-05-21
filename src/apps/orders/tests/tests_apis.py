import json
from datetime import timedelta

from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from model_bakery import baker

from apps.core.tests import BaseAPITestCase
from apps.tasties.models import Tasty
from apps.user.models import Address, User


class OrdersTest(BaseAPITestCase):

    def setUp(self) -> None:
        self.tasty = baker.make(Tasty)
        self.address = baker.make(Address)
        self.user = baker.make(User)
        self.client.force_authenticate(user=self.user)

    def test_create_order_invalid_address_error_400(self):
        order_data = {
            'delivery': timezone.now() + timedelta(days=2),
            'quantity': 2,
            'tasty': self.tasty.id,
            'address': self.address.id
        }

        url = reverse('orders:order-list')
        response = self.client.post(url, data=order_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = json.loads(response.content)
        self.assertEqual(response['address'], [f'Invalid pk "{self.address.pk}" - object does not exist.'])

    def test_create_order_invalid_delivery_date_error_400(self):
        order_data = {
            'delivery': timezone.now(),
            'quantity': 2,
            'tasty': self.tasty.id,
            'address': self.address.id
        }

        url = reverse('orders:order-list')
        response = self.client.post(url, data=order_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = json.loads(response.content)
        self.assertEqual(response['delivery'], ['You can choose your delivery date from the next day.'])


def test_create_order_successful_201(self):
    address_data = {
        'owner': self.user.id
    }
    address = baker.make(Address, **address_data)
    order_data = {
            'delivery': timezone.now() + timedelta(days=2),
            'quantity': 2,
            'tasty': self.tasty.id,
            'address': address.id
    }

    url = reverse('orders:order-list')
    response = self.client.post(url, data=order_data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

