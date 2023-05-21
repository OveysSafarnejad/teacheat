from rest_framework import serializers
from apps.general.models import City


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', )
