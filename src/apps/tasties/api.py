from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
# from drf_yasg.utils import swagger_auto_schema
from apps.core.viewsets import CoreViewSet
from apps.tasties.filters import TastyFilter
from apps.tasties.serializers import (
    TastyFoodInputSerializer,
    ListTastyItemSerializer,
    CreateRatingSerializer,
)
from apps.tasties.querysets import (
    get_all_tasties,
    get_timeline_queryset
)
from apps.tasties.models import Tasty
from apps.tasties import services as tasty_service


class TastyFoodViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    CoreViewSet
):
    model = Tasty
    queryset = get_all_tasties()

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TastyFilter

    serializers = {
        'create': TastyFoodInputSerializer,
        'retrieve': TastyFoodInputSerializer,
        'update': TastyFoodInputSerializer,
        'list': ListTastyItemSerializer,
        'rate': CreateRatingSerializer,
    }

    permissions = {
        'create': IsAuthenticated,
        'list': None,
        'update': IsAuthenticated,
        'like': IsAuthenticated,
        'rate': IsAuthenticated,
    }

    querysets = {
        'list': get_timeline_queryset,
        'update': get_all_tasties,
    }

    def list(self, request, *args, **kwargs):
        user = request.user
        self.queryset = self.filter_queryset(
            get_timeline_queryset(
                user=user if user.is_authenticated else None
            )
        )
        return super(TastyFoodViewSet, self).list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        chef = self.request.user
        self.queryset = self.get_queryset(chef_id=chef.id)
        return super(TastyFoodViewSet, self).update(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     query_serializer=None,
    #     responses={
    #         status.HTTP_200_OK: None
    #     }
    # )
    @action(methods=['POST'], detail=True, url_path='like')
    def like(self, request, *args, **kwargs): # noqa
        tasty = self.get_object()
        user = request.user
        if user.id not in tasty.liked_users_ids:
            tasty_service.like(tasty, user)
        return Response(status=status.HTTP_200_OK)

    # @swagger_auto_schema(
    #     query_serializer=None,
    #     responses={
    #         status.HTTP_200_OK: None
    #     }
    # )
    @action(methods=['POST'], detail=True, url_path='rate')
    def rate(self, request, *args, **kwargs): # noqa
        tasty = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = serializer.validated_data.get('rating')
        user = request.user
        if user.id in tasty.rated_users_ids:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": _('your rating already has been submitted.')
                }
            )
        tasty_service.rate(tasty, user, rating)

        return Response(status=status.HTTP_200_OK)
