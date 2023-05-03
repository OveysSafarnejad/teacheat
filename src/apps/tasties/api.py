from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from apps.core.viewsets import CoreViewSet
from apps.tasties.serializers import CreateTastyFoodItemSerializer


class TastyFoodViewSet(mixins.CreateModelMixin, CoreViewSet):
    serializers = {
        'create': CreateTastyFoodItemSerializer,
    }

    permissions = {
        'create': IsAuthenticated,
    }
