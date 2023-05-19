import os
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import BaseModel
from apps.core.validators import validate_mobile, validate_email
from apps.user.manager import UserManager


def profile_img_path_generator(instance, filename):

    ext = os.path.splitext(filename)[1]
    return os.path.join('profiles/img', f'{uuid.uuid1()}{ext}')


class User(AbstractUser):
    birth = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True, validators=[validate_mobile])
    email = models.CharField(max_length=100, null=False, blank=False, validators=[validate_email], unique=True)
    profile = models.ImageField(null=True, blank=True, upload_to=profile_img_path_generator)
    verified = models.BooleanField(default=False)

    city = models.ForeignKey(
        'general.City',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email'])
        ]

    def __str__(self):
        return self.full_name


class Address(BaseModel):
    title = models.CharField(max_length=50)
    postal_code = models.PositiveSmallIntegerField()
    street = models.CharField(max_length=100)
    house_number = models.PositiveSmallIntegerField()
    apt_number = models.PositiveSmallIntegerField()

    city = models.ForeignKey(
        'general.City',
        on_delete=models.CASCADE
    )

    owner = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        indexes = [
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return f'{self.title} for {self.owner.full_name}'
