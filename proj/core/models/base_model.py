from datetime import datetime

from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self):
        self.deleted_at = datetime.utcnow()
        self.save()
