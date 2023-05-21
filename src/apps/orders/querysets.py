from django.db.models import Avg, Count, Value, functions, F

from apps.orders.models import Order
from apps.user.models import User
from apps.orders.enums import OrderStatusEnum


def get_all_user_orders(owner: User):
    return Order.objects.select_related(
        'tasty',
        'owner',
        'address',
    ).filter(
        owner=owner
    )


def get_user_registered_orders(*query, **filters):
    return get_all_user_orders(
        *query,
        **filters
    ).filter(
        status=OrderStatusEnum.REGISTERED
    )