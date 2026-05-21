
from functools import wraps, lru_cache
from typing import Callable, Any
import threading

@lru_cache(maxsize=128)
def improved_cache(func: Callable) -> Callable:
    '''Thread-safe caching with LRU eviction'''
    cache = {}
    lock = threading.Lock()
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        
        with lock:
            if key in cache:
                return cache[key]
            
            result = func(*args, **kwargs)
            cache[key] = result
            return result
    
    return wrapper
