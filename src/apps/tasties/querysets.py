from django.db.models import QuerySet
from apps.tasties.models import Tasty
from apps.user import services as user_service
from apps.user.models import User


def get_all_tasties() -> QuerySet:
    return Tasty.objects.select_related(
        'chef'
    ).prefetch_related(
        'ingredients',
    ).all()


def get_timeline_queryset(user: User = None, **kwargs) -> QuerySet:
    queryset = kwargs.pop('queryset', None)
    if queryset is None:
        queryset = Tasty.objects

    if user:
        user_tags, user_liked_chef_ids = user_service.get_user_favorites(
            user=user
        )

        tasties_with_liked_tags = queryset.filter(
            tags__overlap=user_tags
        )

        tasties_from_liked_chefs = queryset.filter(
            chef_id__in=user_liked_chef_ids
        )

        others = queryset.exclude(
            id__in=[
                item.id for item in
                tasties_with_liked_tags | tasties_from_liked_chefs
            ]
        )

        return (
                tasties_with_liked_tags | tasties_from_liked_chefs | others
        ).exclude(chef_id=user.id)

    else:
        return queryset.exclude(chef_id=user.id)
