from rest_framework import routers

from apps.orders.api import ChefOrdersViewSet, OrderViewSet


app_name = 'orders'

router = routers.DefaultRouter()
chef_orders_router = routers.DefaultRouter()

# prefix - The URL prefix to use for this set of routes.
# basename - The basename argument is used to specify the initial part of the view name pattern.
# In the example below (order-list), that's the order part.
# Then we can address them by this pattern: namespace:url-name like orders:order-list

router.register(
    prefix='orders',
    viewset=OrderViewSet,
    basename='order'
)

chef_orders_router.register(
    prefix='chef-orders',
    viewset=ChefOrdersViewSet,
    basename='chef-orders'
)
