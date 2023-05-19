from django.contrib import admin

from apps.core.admin import ModelAdminBase
from apps.orders.models import Order
from apps.tasties.models import Tasty
from apps.user.models import Address, User


@admin.register(Order)
class OrderAdmin(ModelAdminBase):
    list_display = ('reference', 'delivery', 'quantity', 'status', 'tasty_id', 'owner_id', 'address_id')
    search_fields = ('reference', 'owner', 'tasty__chef')
    list_filter = ('status',)
    raw_id_fields = ('tasty', 'owner', 'address')
    list_per_page = 10

    def tasty_id(self, entity):
        return self.get_detail_page(Tasty, entity.tasty_id)

    def owner_id(self, entity):
        return self.get_detail_page(User, entity.owner_id)

    def address_id(self, entity):
        return self.get_detail_page(Address, entity.address_id)
