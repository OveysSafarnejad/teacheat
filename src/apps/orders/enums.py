from apps.core.structs import EnumBase, EnumMember
from django.utils.translation import gettext_lazy as _


class OrderStatusEnum(EnumBase):
    REGISTERED = EnumMember(0, _('Registered'))
    REJECTED = EnumMember(1, _('Rejected'))
    CANCELED = EnumMember(2, _('Canceled'))
    ACCEPTED = EnumMember(3, _('Accepted'))
    NOT_ACCEPTED = EnumMember(4, _('Not Accepted'))
