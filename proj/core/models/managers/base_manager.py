
import json

from django.apps import apps
from django.core.serializers import serialize
from django.db import models

from proj.core.fns.etc import noop


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

        return cache

    def _set_cache(self, cache, key, value):
        '''
        Given a key and cache object, set the value in cache for the key.
        '''
        cache[key] = value

    def response(self, results):
        '''
        Subclass this method to transform a response object into a JSON object.
        '''
        results = json.loads(serialize('json', results))
        return results[0] if len(results) == 1 else results
