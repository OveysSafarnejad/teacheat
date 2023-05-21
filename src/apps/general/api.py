from rest_framework.viewsets import mixins

from apps.core.viewsets import CoreViewSet
from apps.general.models import City
from apps.general.serializers import CityListSerializer


class CityViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, CoreViewSet):
    model = City
    queryset = City.objects.all()

    serializers = {
        'list': CityListSerializer
    }
