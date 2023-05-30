# from django.core.exceptions import ValidationError
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import BaseModel
from apps.utils.urilities import generate_slug
from apps.orders.enums import OrderStatusEnum


class Order(BaseModel):

    reference = models.CharField(max_length=12, unique=True)
    delivery = models.DateTimeField()
    quantity = models.PositiveSmallIntegerField(
        default=1,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(5)
        )
    )
    status = models.PositiveSmallIntegerField(
        choices=OrderStatusEnum.to_tuple(),
        default=OrderStatusEnum.REGISTERED
    )

    tasty = models.ForeignKey(
        'tasties.Tasty',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    owner = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='user_orders'
    )
    address = models.ForeignKey(
        'user.Address',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        indexes = [
            models.Index(fields=['reference'])
        ]

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):

        if self.reference in (None, ''):
            self.reference = generate_slug(
                self.__class__,
                search_field='reference',
                length=12
            )

        # if self.delivery < timezone.now() + timezone.timedelta(days=1):
        #     raise ValidationError(
        #         _('Delivery is available for the day after ordering.')
        #     )

        super(Order, self).save()
