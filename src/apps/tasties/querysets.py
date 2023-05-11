from apps.tasties.models import Tasty


def get_all_tasties():
    return Tasty.objects.select_related(
        'chef'
    ).all()
