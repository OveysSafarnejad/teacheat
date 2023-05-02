from django.utils.translation import gettext_lazy as _
from apps.core.structs import EnumBase, EnumMember


class IngredientUnit(EnumBase):
    PINT = EnumMember(0, _('Pint'))
    TABLE_SPOON = EnumMember(1, _('Table Spoon'))
    OUNCE = EnumMember(2, _('Ounce'))
    CUP = EnumMember(3, _('Cup'))
    NUMBERS = EnumMember(4, _('Numbers'))
