from rest_framework import routers
from apps.chef.apis import ChefViewSet

app_name = "chefs"

# prefix - The URL prefix to use for this set of routes.
# basename - The basename argument is used to specify the initial part of the view name pattern.
# In the example below (chef-list), that's the chef part.
# Then we can address them by this pattern: namespace:url-name like chefs:chef-list

router = routers.DefaultRouter()
router.register('chefs', ChefViewSet, basename='chef')
