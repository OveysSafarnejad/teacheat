from django.contrib import admin
from apps.core.admin import ModelAdminBase
from apps.general.models import City


@admin.register(City)
class CityAdmin(ModelAdminBase):
    list_display = ('name',)
