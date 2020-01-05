
from channels.db import database_sync_to_async

from proj.core.fns.etc import noop


def _set_cache(cache, key, value):
    '''
    Given a key and cache object, set the value in cache for the key.
    '''
    cache[key] = value


async def _get_or_fetch_from_cache(
    cache, key, *,
    fetch_func=noop, fetch_args=(), fetch_kwargs={}
):
    '''
    Given a key and cache object, get or fetch that object.
    '''
    cache = cache or {}

    if key in cache:
        result = cache[key]
    else:
        result = await database_sync_to_async(fetch_func)(*fetch_args, **fetch_kwargs)
        try:
            result = result[0]
        except Exception:
            pass
        _set_cache(cache, key, result)

    return cache
