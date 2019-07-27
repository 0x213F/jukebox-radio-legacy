
import json
import random
import string

from datetime import datetime

from django.core.serializers import serialize
from django.db.models import F
from django.db.models import Q

from proj.core.models.managers import BaseManager


class AlbumManager(BaseManager):
    '''
    todo: docstring
    '''
    pass
