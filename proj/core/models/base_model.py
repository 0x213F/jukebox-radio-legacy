from datetime import datetime

from django.db import models


class BaseModel(models.Model):
    '''
    Inherits from Django Model.
    '''

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self):
        self.deleted_at = datetime.utcnow()
        self.save()
