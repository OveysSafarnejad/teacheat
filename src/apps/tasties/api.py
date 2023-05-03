from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from apps.core.viewsets import CoreViewSet
from apps.tasties.serializers import (
    CreateTastyFoodItemSerializer,
    ListTastyItemSerializer,
    CreateRatingSerializer,
)
from apps.tasties.querysets import get_all_tasties
from apps.tasties.models import Tasty
from apps.tasties import services as tasty_service


class TastyFoodViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    CoreViewSet
):
    model = Tasty
    queryset = get_all_tasties()
    serializers = {
        'create': CreateTastyFoodItemSerializer,
        'list': ListTastyItemSerializer,
        'rate': CreateRatingSerializer,
    }

    permissions = {
        'create': IsAuthenticated,
        'list': None,
        'like': IsAuthenticated,
        'rate': IsAuthenticated,
    }

    querysets = {
        'list': get_all_tasties()
    }

    @swagger_auto_schema(
        query_serializer=None,
        responses={
            status.HTTP_200_OK: None
        }
    )
    @action(methods=['POST'], detail=True, url_path='like')
    def like(self, request, *args, **kwargs):
        tasty = self.get_object()
        user = request.user
        if user.id not in tasty.liked_users_ids:
            tasty_service.like(tasty, user)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        query_serializer=None,
        responses={
            status.HTTP_200_OK: None
        }
    )
    @action(methods=['POST'], detail=True, url_path='rate')
    def rate(self, request, *args, **kwargs):
        tasty = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = serializer.validated_data.get('rating')
        user = request.user
        if user.id in tasty.rated_users_ids:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": _('your rating already has been submited.')
                }
            )
        tasty_service.rate(tasty, user, rating)

        return Response(status=status.HTTP_200_OK)
