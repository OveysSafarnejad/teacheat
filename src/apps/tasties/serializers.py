from rest_framework import serializers
from apps.tasties.models import Rating, Tasty


class CreateTastyFoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasty
        fields = ('id', 'title', 'img', 'recipe', 'duration', 'tags', 'category',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data["chef"] = self.context["request"].user
        return super().create(validated_data)

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
