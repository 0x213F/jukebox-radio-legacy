
import json

from django.core.serializers import serialize
from django.db import models


class BaseManager(models.Manager):
    '''
    Inherits from Django Manager.
    '''
    pass
