from rest_framework import serializers
from apps.tasties.models import Tasty


class CreateTastyFoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasty
        fields = ('id', 'title', 'img', 'recepie', 'duration', 'tags', 'category',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data["chef"] = self.context["request"].user
        return super().create(validated_data)

    def to_representation(self, instance):
        repr_data = super().to_representation(instance)
        repr_data['category'] = instance.category.name
        return repr_data
