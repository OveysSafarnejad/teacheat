import os
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.validators import validate_mobile, validate_email


def profile_img_path_generator(instance, filename):

    ext = os.path.splitext(filename)[1]
    return os.path.join('profiles/img', f'{uuid.uuid1()}{ext}')


class User(AbstractUser):
    birth = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True, validators=[validate_mobile])
    email = models.CharField(max_length=100, null=False, blank=False, validators=[validate_email], unique=True)
    profile = models.ImageField(null=True, blank=True, upload_to=profile_img_path_generator)
    verified = models.BooleanField(default=False)

    city = models.ForeignKey('general.City', null=True, blank=True, on_delete=models.PROTECT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    # objects = user_manager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email'])
        ]
