from _typeshed import Incomplete
from collections import OrderedDict
from collections.abc import Hashable
from typing import Any, Callable, NamedTuple

logger: Incomplete

class LRUCache:
    """LRU cache where you can control how many slots are available, maximum memory to use for the cache, and a cache
    time out for the items.

    :param max_entries: The maximum number of entries the cache can hold.
    :param max_memory: The maximum memory to use for the cache, in bytes. If set to 0, the cache will not use memory
        limits.
    :param time_out: The time out for the items in the cache, in seconds. If set to 0, the items will never expire.

    The stats() method will return a dictionary of important statistics about the cache.
    The clear() method will clear the cache and reset all statistics.
    """

    class LRUEntry(NamedTuple):
        timestamp: Incomplete
        value: Incomplete
    cache: OrderedDict[Any, LRUCache.LRUEntry]
    max_entries: Incomplete
    max_memory: Incomplete
    time_out: Incomplete
    def __init__(self, max_entries: int, max_memory: int = 0, time_out: float = 0.0) -> None: ...
    current_memory_usage: int
    hits: int
    misses: int
    inserts: int
    evictions_slots: int
    evictions_time: int
    evictions_memory: int
    def clear(self) -> None: ...
    def get(self, key: Hashable) -> Any: ...
    def set(self, key: Hashable, value: object) -> None: ...
    def delete(self, key: Hashable) -> None: ...
    def remove_oldest_item(self) -> None: ...
    def expires_in(self, key: str) -> int | None: ...
    def stats(self) -> dict[str, int]: ...

def lru_cache(max_entries: int, max_memory_in_bytes: int, time_threshold_in_seconds: float, time_out_in_seconds: float = 0.0) -> Callable:
    """Decorator to add an LRU cache to a function.

    The decorator can control the number of cache slots (max_entries) and how much memory to use for cached element
    (max_memory).

    In addition, the decorator can set how long a function execution must take before the result is cached
    (time_threshold), to avoid caching results that are fast to compute or retrieve, thus only using the cache for
    slower items.

    The time_out parameter can be used to set how long each cached item should remain valid. If set to 0, the items will
    never expire.

    """
LRUFuncCache = lru_cache
