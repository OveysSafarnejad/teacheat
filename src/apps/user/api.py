from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import mixins
from apps.core.viewsets import CoreViewSet
from apps.user.serializers import (
    UserSignUpSerializer,
    UserAddressesSerializer
)
from apps.user.models import Address


class UserViewSet(mixins.CreateModelMixin, CoreViewSet):

    serializers = {
        'create': UserSignUpSerializer,
    }


class AddressViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    CoreViewSet
):

    model = Address
    permission_classes = (IsAuthenticated, )

    serializer_class = UserAddressesSerializer

    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(owner=user).order_by('created_time')
