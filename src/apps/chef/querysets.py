from django.db.models import Avg, Count, Value, functions, F
from apps.user.models import User


def get_chefs():
    """
    filters users if the use has at least one tasty food
    """

    chefs = User.objects.prefetch_related(
        'tasties',
        'tasties__ratings'
    ).annotate(
        number_of_tasties=Count("tasties")
    ).annotate(
        overal_rating=Avg('tasties__ratings__rating')
    ).annotate(
        chef_name=functions.Concat(F('first_name'), Value(' '), F('last_name'))
    ).filter(
        number_of_tasties__gt=0
    ).order_by(
        '-number_of_tasties'
    )

    return chefs
