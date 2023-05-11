from django_filters import rest_framework as filters
from django.db.models import Q


class ChefFilter(filters.FilterSet):
    chef_name = filters.CharFilter(
        label='chef_name',
        method='chef_name_filter',
    )

    rating = filters.RangeFilter(
        label='rating',
        method='rating_filter'
    )

    city = filters.CharFilter(
        label='city',
        method='city_filter'
    )

    def chef_name_filter(self, queryset, name, value):
        return queryset.filter(chef_name__icontains=value)

    def rating_filter(self, queryset, name, value):
        return queryset.filter(
            Q(overal_rating__gte=value.start) & Q(overal_rating__lte=value.stop)
        )

    def city_filter(self, queryset, name, value):
        return queryset.filter(city__name__icontains=value)
