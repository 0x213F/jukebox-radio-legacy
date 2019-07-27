
import json

from django.core.serializers import serialize
from django.db import models


class BaseManager(models.Manager):
    '''
    Inherits from Django Manager.
    '''

    def response(self, results):
        '''
        Subclass this method to transform a response object into a JSON object.
        '''
        results = json.loads(serialize('json', results))
        return results[0] if len(results) == 1 else results
