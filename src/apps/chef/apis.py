from django_filters import rest_framework as filters
from apps.core.viewsets import CoreViewSet
from rest_framework.viewsets import mixins
from apps.chef.serializers import ChefListSerializer
from apps.chef.querysets import get_chefs
from apps.chef.filters import ChefFilter


class ChefViewSet(mixins.ListModelMixin, CoreViewSet):

    serializers = {
        'list': ChefListSerializer,
    }

    permissions = {
        'list': None
    }

    querysets = {
        'list': get_chefs,
    }

    filter_backends = [filters.DjangoFilterBackend, ]
    filterset_class = ChefFilter
