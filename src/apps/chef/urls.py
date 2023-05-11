from rest_framework import routers
from apps.chef.apis import ChefViewSet

app_name = "chefs"

router = routers.DefaultRouter()
router.register('chefs', ChefViewSet, basename='chefs')
