from uuid import uuid1
from datetime import datetime, timedelta

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.orders.models import Order


class OrderCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ('id', 'delivery', 'quantity', 'tasty', 'address', 'owner', 'status')
        read_only_fields = ('id', 'status', )
        extra_kwargs = {
            'quantity': {
                'required': True,
            }
        }

    @staticmethod
    def validate_delivery(delivery_date: datetime) -> datetime:
        if delivery_date < timezone.now() + timedelta(days=1):
            raise ValidationError(
                _(f'You can choose your delivery date from the next day.')
            )
        return delivery_date

    def validate_address(self, address) -> uuid1:
        if address.owner.id is not self.context['request'].user.id:
            raise ValidationError(
                _(f'Invalid pk \"{address.id}\" - object does not exist.')
            )
        return address
