from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.viewsets import mixins
from rest_framework.response import Response

from apps.core.viewsets import CoreViewSet
from apps.orders.models import Order
from apps.orders.serializers import (
    OrderCreateSerializer,
    UserOrderListSerializer,
)
from apps.orders.querysets import (
    get_all_user_orders,
    get_user_registered_orders,
)
from apps.orders.enums import OrderStatusEnum


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    CoreViewSet
):

    model = Order
    permission_classes = (IsAuthenticated, )

    serializers = {
        'create': OrderCreateSerializer,
        'list': UserOrderListSerializer,
        'retrieve': UserOrderListSerializer,
    }

    querysets = {
        'destroy': get_user_registered_orders
    }

    def get_queryset(self, **kwargs):

        """
        base queryset for entire ViewSet
        It's changeable through querysets field from CoreViewSet
        """

        return get_all_user_orders(
            owner=self.request.user
        )

    def destroy(self, request, *args, **kwargs):
        self.queryset = get_user_registered_orders(owner=request.user.id)
        order = self.get_object()
        order.status = OrderStatusEnum.CANCELED
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)