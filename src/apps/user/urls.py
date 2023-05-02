from rest_framework import routers
from apps.user.api import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, 'Users')
