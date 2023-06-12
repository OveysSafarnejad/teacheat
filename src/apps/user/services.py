from apps.tasties.models import Like
from apps.user.models import User


def get_user_favorites(user: User) -> tuple:
    """Takes user, returns user liked tags (tasties)"""

    query_data = Like.objects.filter(
        user=user
    ).select_related(
        'tasty__tags',
        'tasty__chef_id'
    ).only(
        'tasty__tags',
        'tasty__chef_id'
    ).values_list('tasty__tags', 'tasty__chef_id')

    return (
        [tag for like_item in query_data for tag in like_item[0]],
        [like_item[1] for like_item in query_data]
    )
