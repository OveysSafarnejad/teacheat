from rest_framework import routers
from apps.tasties.api import TastyFoodViewSet

router = routers.DefaultRouter()
router.register('tasty-foods', TastyFoodViewSet, 'Tasty Food')
