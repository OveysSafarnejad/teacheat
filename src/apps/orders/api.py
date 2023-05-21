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
    get_all_user_orders
)


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
    }

    def get_queryset(self, **kwargs):

        """
        base queryset for entire ViewSet
        It's changeable through querysets field from CoreViewSet
        """

        return get_all_user_orders(
            owner=self.request.user
        )


