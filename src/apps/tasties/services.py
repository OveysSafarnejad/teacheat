from apps.tasties.models import Like, Rating


def like(tasty, user) -> None:
    """
    accepts a tasty instance and increase it's likes by one

    :param tasty: Tasty
    :param user: User

    :rtype None
    """
    Like.objects.create(tasty=tasty, user=user)


def rate(tasty, user, rating) -> None:
    """
    accepts a tasty instance and submits a rating for that

    :param tasty: Tasty
    :param user: User

    :rtype None
    """
    Rating.objects.create(tasty=tasty, user=user, rating=rating)
