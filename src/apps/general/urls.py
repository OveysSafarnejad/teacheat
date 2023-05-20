from rest_framework import routers

from apps.general.api import CityViewSet


app_name = 'general'

# prefix - The URL prefix to use for this set of routes.
# basename - The basename argument is used to specify the initial part of the view name pattern.
# In the example below (city-list), that's the city part.
# Then we can address them by this pattern: namespace:url-name like general:city-list

router = routers.DefaultRouter()
router.register(
    prefix='cities',
    viewset=CityViewSet,
    basename='city'
)
