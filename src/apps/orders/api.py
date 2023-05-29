from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import mixins
from rest_framework.response import Response

from apps.core.viewsets import CoreViewSet
from apps.orders.models import Order
from apps.orders.serializers import (
    OrderCreateSerializer,
    OrderListSerializer,
)
from apps.orders.querysets import (
    get_all_orders,
    get_all_user_orders,
    get_all_user_registered_orders,

    get_all_chef_orders,
    get_all_chef_valid_orders,
)
from apps.orders.enums import OrderStatusEnum


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    CoreViewSet
):

    model = Order
    permission_classes = (IsAuthenticated, )

    serializers = {
        'create': OrderCreateSerializer,
        'list': OrderListSerializer,
        'retrieve': OrderListSerializer,
    }

    querysets = {
        'create': get_all_orders,
        'list': get_all_user_orders,
        'retrieve': get_all_user_orders,
        'destroy': get_all_user_registered_orders,
    }

    def get_queryset(self, **kwargs):
        """
        base queryset for entire ViewSet
        It's changeable through querysets field from CoreViewSet
        """

        return super().get_queryset(owner=self.request.user, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # default self.get_queryset() applies this filter
        # self.queryset = super().get_queryset(owner=request.user)

        order = self.get_object()
        order.status = OrderStatusEnum.CANCELED
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChefOrdersViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    CoreViewSet
):
    model = Order
    permission_classes = (IsAuthenticated, )
    serializers = {
        'list': OrderListSerializer,
    }

    querysets = {
        'list': get_all_chef_orders,
        'destroy': get_all_chef_valid_orders,
        'partial_update': get_all_chef_valid_orders,
    }

    def get_queryset(self, **kwargs):

        return super().get_queryset(
            tasty__chef=self.request.user,
            **kwargs
        )

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        order.status = OrderStatusEnum.ACCEPTED
        order.save()
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        # TODO: adding auto-cancel order 24 hour before its delivery
        order = self.get_object()
        order.status = OrderStatusEnum.REJECTED
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
