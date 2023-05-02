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


class FoodCategory(BaseModel):
    name = models.CharField(max_length=20)

    @property
    def number_of_foods(self):
        return 0

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name
