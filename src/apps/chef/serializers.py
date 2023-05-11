from rest_framework import serializers


class ChefListSerializer(serializers.Serializer):

    user_info = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    tasties = serializers.SerializerMethodField()

    @staticmethod
    def get_user_info(chef):
        return dict(
            profile_image=chef.profile if chef.profile else None,
            chef_name=chef.full_name,
            user_id=chef.id,
            verified=chef.verified,
        )

    @staticmethod
    def get_city(chef):
        return dict(
            city_id=chef.city.id,
            city=chef.city.name
        ) if chef.city else None

    @staticmethod
    def get_rating(chef):
        return chef.overal_rating

    @staticmethod
    def get_tasties(chef):
        return chef.number_of_tasties
