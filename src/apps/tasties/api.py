from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from apps.core.viewsets import CoreViewSet
from apps.tasties.serializers import (
    CreateTastyFoodItemSerializer,
    ListTastyItemSerializer,
)
from apps.tasties.querysets import get_all_tasties


class TastyFoodViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    CoreViewSet
):
    serializers = {
        'create': CreateTastyFoodItemSerializer,
        'list': ListTastyItemSerializer,
    }

    permissions = {
        'create': IsAuthenticated,
        'list': None,
    }

    querysets = {
        'list': get_all_tasties()
    }
