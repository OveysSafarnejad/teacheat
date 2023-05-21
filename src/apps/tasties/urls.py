from rest_framework import routers
from apps.tasties.api import TastyFoodViewSet


app_name = "tasties"

# prefix - The URL prefix to use for this set of routes.
# basename - The basename argument is used to specify the initial part of the view name pattern.
# In the example below (tasty-list), that's the tasty part.
# Then we can address them by this pattern: namespace:url-name like general:tasty-list

router = routers.DefaultRouter()
router.register(
    prefix='tasties',
    viewset=TastyFoodViewSet,
    basename='tasty'
)
