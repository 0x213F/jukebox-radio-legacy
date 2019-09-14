
import json

from django.apps import apps
from django.core.serializers import serialize
from django.db import models


def noop(*args, **kwargs):
    pass


class BaseManager(models.Manager):
    '''
    Inherits from Django Manager.
    '''

    def _get_or_fetch_from_cache(
        self, cache, key, *,
        fetch_func=noop, fetch_args=(), fetch_kwargs={}
    ):
        '''
        Given a key and cache object, get or fetch that object.
        '''
        cache = cache or {}

        if key in cache:
            result = cache[key]
        else:
            result = fetch_func(*fetch_args, **fetch_kwargs)
            try:
                result = result[0]
            except Exception:
                pass
            cache[key] = result
            print(cache)

        return cache

    def response(self, results):
        '''
        Subclass this method to transform a response object into a JSON object.
        '''
        results = json.loads(serialize('json', results))
        return results[0] if len(results) == 1 else results
