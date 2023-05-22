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
