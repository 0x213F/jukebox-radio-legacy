
from django.db import models


class BaseModel(models.Model):

    class Meta:
        abstract = True

    RESULT_TRUE = 0
    RESULT_FALSE = 1
    RESULT_INCONCLUSIVE = 2
