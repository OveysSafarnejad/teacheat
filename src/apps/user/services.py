from apps.tasties.models import Like
from apps.user.models import User


def get_user_favorite_tags(user: User) -> list:
    """Takes user, returns user liked tags (tasties)"""

    liked_tasties_tags = Like.objects.filter(
        user=user
    ).select_related(
        'tasty__tags'
    ).only(
        'tasty__tags'
    ).values_list('tasty__tags', flat=True).first()

    return liked_tasties_tags
