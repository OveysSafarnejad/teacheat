from django.utils import timezone
from apps.orders.models import Order
from apps.orders.enums import OrderStatusEnum


def get_all_orders():
    return Order.objects.all()


def get_all_user_orders():
    return get_all_orders().select_related(
        'tasty',
        'owner',
        'address',
    )


def get_all_user_registered_orders():
    return get_all_orders().filter(
        status=OrderStatusEnum.REGISTERED
    )


def get_all_chef_orders():
    return get_all_orders().select_related(
        'owner',
        'address',
    )


def get_all_chef_valid_orders():
    return get_all_orders().filter(
        delivery__gt=timezone.now() + timezone.timedelta(days=1),
        status=OrderStatusEnum.REGISTERED
    )
