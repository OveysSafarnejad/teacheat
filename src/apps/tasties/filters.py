from django_filters import rest_framework as filters
from django.db.models import Value, functions, F
from apps.tasties.models import Tasty
from apps.user.models import User


class TastyFilter(filters.FilterSet):
    chef_name = filters.CharFilter(
        lookup_expr='icontains',
        label='chef_name',
        method='chef_name_filter'
    )

    class Meta:
        model = Tasty
        fields = {
            'title': ['iexact'],
            'chef': ['exact'],
        }

    def chef_name_filter(self, queryset, name, value):
        filtered_chefs = User.objects.annotate(
            full_name=functions.Concat(F('first_name'), Value(' '), F('last_name'))
        ).filter(full_name__icontains=value)
        return queryset.filter(chef_id__in=filtered_chefs)
