from rest_framework import routers

from apps.general.api import CityViewSet


app_name = 'general'

router = routers.DefaultRouter()
router.register('cities', CityViewSet, 'cities')
