import json
from datetime import timedelta

from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from model_bakery import baker

from apps.core.tests import BaseAPITestCase
from apps.tasties.models import Tasty
from apps.user.models import Address, User
from apps.orders.models import Order
from apps.orders.enums import OrderStatusEnum


class OrdersTest(BaseAPITestCase):

    def setUp(self) -> None:
        self.tasty = baker.make(Tasty)
        self.address = baker.make(Address)
        self.user = baker.make(User)

        address_data = {
            'owner': self.user
        }
        self.client_user_address = baker.make(Address, **address_data)
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

        order_data = {
                'delivery': timezone.now() + timedelta(days=2),
                'quantity': 2,
                'tasty': self.tasty.id,
                'address': self.client_user_address.id
        }

        url = reverse('orders:order-list')
        response = self.client.post(url, data=order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_order_by_id_successful_200(self):
        order_data = {
            'delivery': timezone.now() + timedelta(days=2),
            'owner': self.user
        }
        order = baker.make(Order, **order_data)
        url = reverse('orders:order-detail', kwargs={
            'pk': str(order.id)
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)
        self.assertEqual(response['reference'], order.reference)

    def test_get_order_by_invalid_id_404(self):
        order_data = {
            'delivery': timezone.now() + timedelta(days=2),
        }
        order = baker.make(Order, **order_data)
        url = reverse('orders:order-detail', kwargs={
            'pk': str(order.id)
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_users_orders_successful_200(self):
        order_data = {
            'delivery': timezone.now() + timedelta(days=2),
            'quantity': 2,
            'tasty': self.tasty,
            'address': self.client_user_address,
            'owner': self.user
        }

        baker.make(Order, **order_data)
        url = reverse('orders:order-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)
        self.assertEqual(len(response), 1)

    def test_cancel_order_successful_204(self):
        order_data = {
            'delivery': timezone.now() + timedelta(days=2),
            'quantity': 2,
            'tasty': self.tasty,
            'address': self.client_user_address,
            'owner': self.user,
            'status': 0
        }

        order = baker.make(Order, **order_data)
        url = reverse('orders:order-detail', kwargs={
            'pk': str(order.id)
        })
        response = self.client.delete(url)
        order = Order.objects.get(id=str(order.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(order.status, OrderStatusEnum.CANCELED)

    def test_cancel_order_invalid_status_404(self):
        order_data = {
            'delivery': timezone.now() + timedelta(days=2),
            'quantity': 2,
            'tasty': self.tasty,
            'address': self.client_user_address,
            'owner': self.user,
            'status': 1
        }

        order = baker.make(Order, **order_data)
        url = reverse('orders:order-detail', kwargs={
            'pk': str(order.id)
        })
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cancel_order_invalid_owner_404(self):
        order_data = {
            'delivery': timezone.now() + timedelta(days=2),
            'quantity': 2,
            'tasty': self.tasty,
            'address': self.client_user_address,
            'status': 0
        }

        order = baker.make(Order, **order_data)
        url = reverse('orders:order-detail', kwargs={
            'pk': str(order.id)
        })
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



