from django.db import models
from apps.core.models import BaseModel


class City(BaseModel):
    name = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self) -> str:
        return self.name
