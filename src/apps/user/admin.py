from django.contrib import admin
from apps.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'city')
    list_display_links = ('email',)
    raw_id_fields = ('city',)
    list_per_page = 10
