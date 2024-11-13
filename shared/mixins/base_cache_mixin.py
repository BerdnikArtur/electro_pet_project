from django.core.cache import cache
from django.db.models.manager import BaseManager
from django.utils.encoding import force_bytes

from typing import Any, Callable
from functools import wraps
import hashlib
import inspect


class BaseCachingMixin:
    cache_timeout = 60 * 15  

    def _cache_key(self, key: str) -> str:
        """Generate a cache key."""
        key = hashlib.md5(force_bytes(key)).hexdigest()
        return f"cache_{key}"

    @staticmethod
    def cache_result(key_template: str) -> Callable:
        """Retrieve data from cache or compute it if not cached."""
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                # Get the function signature and bind the arguments
                sig = inspect.signature(func)
                bound_args = sig.bind(self, *args, **kwargs)
                bound_args.apply_defaults()

                # combine args and kwargs and exclude 'self' from the arguments
                bound_arguments = {k: v for k, v in bound_args.arguments.items() if k != 'self'}

                key = key_template.format(**bound_arguments)
                cache_key = self._cache_key(key)
                cached_data = cache.get(cache_key)
                if not cached_data:
                    cached_data = func(self, *args, **kwargs)
                    cache.set(cache_key, cached_data, self.cache_timeout)
                return cached_data
            return wrapper
        return decorator
    
    def get_cached_query(self, key: str, query: BaseManager[Any]):
        cache_key = self._cache_key(key)
        cached_data = cache.get(cache_key)
        if not cached_data:
            cached_data = list(query)
            cache.set(cache_key, cached_data, self.cache_timeout)
        return cached_data