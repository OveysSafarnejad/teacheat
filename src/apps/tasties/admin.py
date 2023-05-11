from django.contrib import admin
from apps.general.models import FoodCategory
from apps.tasties.models import Ingredient, Tasty
from apps.user.models import User
from apps.core.admin import ModelAdminBase


@admin.register(Ingredient)
class IngredientAdmin(ModelAdminBase):
    list_display = ('name', 'volume', 'unit', 'tasty_id',)
    list_display_links = ('name',)
    raw_id_fields = ('tasty',)
    list_per_page = 10

    def tasty_id(self, entity):
        return self.get_detail_page(Tasty, entity.tasty)


@admin.register(Tasty)
class TastyAdmin(ModelAdminBase):

    model = Tasty
    list_display = ('title', 'duration', 'category_id', 'chef_id', 'ingredients')
    list_display_links = ('title',)
    raw_id_fields = ('chef', 'category',)
    list_per_page = 10

    def chef_id(self, entity):
        return self.get_detail_page(User, entity.chef_id)

    def category_id(self, entity):
        return self.get_detail_page(FoodCategory, items_title=entity.category.name, pk=entity.category_id)

    def ingredients(self, entity):
        return self.get_list_page(Ingredient, 'tap to watch', tasty=entity.id)
