import uuid
from functools import wraps

from django.db import models
from django.utils.translation import gettext as _
from apps.utils.users import current_user


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Create time"))
    modified_time = models.DateTimeField(auto_now=True, verbose_name=_("Modify time"))
    creator = models.ForeignKey(
        'user.User',
        related_name="%(app_label)s_%(class)s_created_by_user_id",
        related_query_name="%(app_label)s_%(class)s_created_by_user",
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_("Creator"),
    )
    modifier = models.ForeignKey(
        'user.User',
        related_name="%(app_label)s_%(class)s_updated_by_user_id",
        related_query_name="%(app_label)s_%(class)s_updated_by_user",
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_("Modifier"),
    )
    auto_cols = ['create_time', 'creator', 'modify_time', 'modifier']

    def save(self, **kwargs) -> object:
        self.modifier = current_user.get_current_authenticated_user()
        if not self.id:
            self.id = uuid.uuid1()

        if not self.creator:
            self.creator = current_user.get_current_authenticated_user()

        super().save(**kwargs)

    class Meta:
        ordering = ('-create_time',)
        abstract = True


def skip_signal():
    def _skip_signal(signal_func):
        @wraps(signal_func)
        def _decorator(sender, instance, **kwargs):
            if hasattr(instance, 'skip_signal') and instance.skip_signal:
                return None
            return signal_func(sender, instance, **kwargs)

        return _decorator

    return _skip_signal
