from rest_framework import routers
from apps.user.api import AddressViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, 'Users')
router.register('addresses', AddressViewSet, 'Addresses')