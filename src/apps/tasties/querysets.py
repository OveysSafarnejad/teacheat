from apps.tasties.models import Tasty
from django.db.models.functions import Concat
from django.db.models import Value as V
from django.db.models import F


def get_all_tasties():
    return Tasty.objects.select_related(
        'chef'
    ).all()
