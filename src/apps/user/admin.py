from django.contrib import admin
from apps.user.models import Address, User
from apps.core.admin import ModelAdminBase


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'city')
    list_display_links = ('email',)
    raw_id_fields = ('city',)
    list_per_page = 10


@admin.register(Address)
class UserAdmin(ModelAdminBase):
    list_display = ('title', 'owner_id')
    list_display_links = ('title',)
    raw_id_fields = ('owner',)
    list_per_page = 10

    def owner_id(self, entity):
        return self.get_detail_page(User, entity.owner)
