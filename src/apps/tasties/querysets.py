from django.db.models import QuerySet
from apps.tasties.models import Tasty


def get_all_tasties() -> QuerySet:
    return Tasty.objects.select_related(
        'chef'
    ).prefetch_related(
        'ingredients',
    ).all()
