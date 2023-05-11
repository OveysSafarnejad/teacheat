from django.contrib import admin
from apps.core.admin import ModelAdminBase
from apps.general.models import City, FoodCategory


@admin.register(City)
class CityAdmin(ModelAdminBase):
    list_display = ('name',)


@admin.register(FoodCategory)
class FoodCategoryAdmin(ModelAdminBase):
    list_display = ('name',)
