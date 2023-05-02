import os
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from apps.core.models import BaseModel


def generate_image_path_for_tasty(instance, filename):
    ext = os.path.splitext(filename)[1]
    return os.path.join('tasties/images', f'{uuid.uuid1()}{ext}')


class Ingredient(BaseModel):
    volume = models.PositiveSmallIntegerField()
    unit = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100)
    tasty = models.ForeignKey('tasties.Tasty', on_delete=models.CASCADE, related_name='ingredients')

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        indexes = [
            models.Index(fields=['name'])
        ]


class Tasty(BaseModel):
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to=generate_image_path_for_tasty)
    # video
    likes = models.PositiveIntegerField(default=0)
    recepie = models.TextField()
    duration = models.PositiveSmallIntegerField()
    tags = ArrayField(models.CharField(max_length=15))

    chef = models.ForeignKey('user.User', on_delete=models.PROTECT, related_name='tasties')
    category = models.ForeignKey('general.FoodCategory', on_delete=models.PROTECT, related_name='tasties')

    @property
    def overal_score(self):
        """
        A possitive integer in range(0,5)
        It will be calculated based on user ratings

        :rtype: int
        """
        return 0

    @property
    def ingredients_count(self):
        return self.ingredients.count()

    class Meta:
        verbose_name = 'Tasty'
        verbose_name_plural = 'Tasties'
        indexes = [
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return self.title
