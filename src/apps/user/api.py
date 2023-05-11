from rest_framework.viewsets import mixins
from apps.core.viewsets import CoreViewSet
from apps.user.serializers import UserSignUpSerializer


class UserViewSet(mixins.CreateModelMixin, CoreViewSet):

    serializers = {
        'create': UserSignUpSerializer,
    }
