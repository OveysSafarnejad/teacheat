from django.utils import timezone

from teacheat.celery import celery
from apps.orders.models import Order
from apps.orders.enums import OrderStatusEnum


@celery.task()
def cancel_unaccepted_orders():
    """

    Filters registered orders that are not accepted by chef, and it's delivery
    is less than a dey, then updates them to `NOT_ACCEPTED` status.

    :rtype: dict
    """

    unaccepted_orders = Order.objects.filter(
        delivery__lte=timezone.now() + timezone.timedelta(days=1),
        status=OrderStatusEnum.REGISTERED
    )

    for item in unaccepted_orders:
        item.status = OrderStatusEnum.NOT_ACCEPTED
        item.save()

    return dict(
        time=timezone.now().strftime("%m/%d/%Y, %H:%M:%S"),
        number_of_unaccepted=len(unaccepted_orders)
    )
