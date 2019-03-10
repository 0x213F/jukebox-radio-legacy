
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from .managers import UserManager
from .querysets import UserQuerySet


class User(AbstractUser):

    objects = UserManager.from_queryset(UserQuerySet)()

    phone = models.CharField(
        max_length=32,
        null=True,
        unique=True,
    )

    pin = models.CharField(
        max_length=4,
    )
