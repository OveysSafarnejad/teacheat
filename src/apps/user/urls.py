from rest_framework import routers
from apps.user.api import AddressViewSet, UserViewSet


app_name = 'accounts'

router = routers.DefaultRouter()

# prefix - The URL prefix to use for this set of routes.
# basename - The basename argument is used to specify the initial part of the view name pattern.
# In the example below (user-list), that's the user part.
# Then we can address them by this pattern: namespace:url-name like general:city-list

router.register(
    prefix='users',
    viewset=UserViewSet,
    basename='user'
)

router.register(
    prefix='addresses',
    viewset=AddressViewSet,
    basename='address'
)
