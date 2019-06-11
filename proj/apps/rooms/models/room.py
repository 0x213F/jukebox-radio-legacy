
import datetime
import random
import uuid

from django.conf import settings
from django.db import models
from django.forms import fields

from proj.apps.rooms.models.managers import RoomManager
from proj.apps.rooms.models.querysets import RoomQuerySet

from proj.core.models import BaseModel


class Room(BaseModel):

    # - - - - - - - -
    # config model
    # - - - - - - - -

    class Meta:
        abstract = False

    objects = RoomManager.from_queryset(RoomQuerySet)()

    # - - - - - - - - -
    # fields
    # - - - - - - - - -
