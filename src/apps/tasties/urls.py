from rest_framework import routers
from apps.tasties.api import TastyFoodViewSet


app_name = "tasties"

router = routers.DefaultRouter()
router.register(prefix='tasties', viewset=TastyFoodViewSet, basename='tasties')
