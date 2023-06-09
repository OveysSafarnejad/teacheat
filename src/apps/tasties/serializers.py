from rest_framework import serializers

from apps.tasties.models import Ingredient, Rating, Tasty
from apps.tasties.enums import IngredientUnit


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'volume', 'unit', 'name')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        repr_data = super().to_representation(instance)
        repr_data['unit'] = IngredientUnit(instance.unit)
        return repr_data


class TastyFoodInputSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(
        many=True,
        allow_empty=False,
        allow_null=False
    )

    class Meta:
        model = Tasty
        fields = (
            'id', 'title', 'img', 'recipe', 'duration', 'tags', 'category',
            'ingredients'
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            "img": {
                "required": False
            }
        }

    def create(self, validated_data):
        validated_data["chef"] = self.context["request"].user
        ingredient_data = validated_data.pop('ingredients')
        tasty = super().create(validated_data)
        for ingredient in ingredient_data:
            Ingredient.objects.create(tasty=tasty, **ingredient)

        return tasty

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance = super(TastyFoodInputSerializer, self).update(
            instance,
            validated_data
        )

        instance.ingredients.all().delete()
        for ingredient in ingredients:
            Ingredient.objects.create(tasty=instance, **ingredient)

        return instance

    def to_representation(self, instance):
        repr_data = super().to_representation(instance)
        repr_data['category'] = instance.category.name
        return repr_data


class ListTastyItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Tasty
        fields = ('id', 'title', 'img', 'recipe', 'tags', 'category', 'chef')


class CreateRatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ('rating',)
        extra_kwargs = {
            'rating': {
                "required": True
            }
        }


class TastyBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasty
        fields = ('id', 'title', 'duration', 'chef')
