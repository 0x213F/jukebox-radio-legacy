
from proj.core.fns.etc import noop


def _get_or_fetch_from_cache(
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
        result = fetch_func(*fetch_args, **fetch_kwargs)
        try:
            result = result[0]
        except Exception:
            pass
        cache[key] = result

    return cache
