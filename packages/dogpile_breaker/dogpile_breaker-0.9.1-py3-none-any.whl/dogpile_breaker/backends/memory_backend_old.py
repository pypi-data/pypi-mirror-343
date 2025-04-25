import asyncio
import time
from collections import OrderedDict
from contextlib import suppress


class MemoryBackend:
    def __init__(self, max_size: int = 1000) -> None:
        self.max_size = max_size
        self._cache: OrderedDict[str, tuple[bytes, float, float]] = OrderedDict()
        self._distributed_locks: dict[str, tuple[bytes, float, float]] = {}

    async def initialize(self) -> None:
        return

    async def aclose(self) -> None:
        self._cache.clear()
        self._distributed_locks.clear()

    async def get_serialized(self, key: str) -> bytes | None:
        if key in self._cache:
            self._cache.move_to_end(key)
            data, created_at, ttl = self._cache[key]
            if time.time() < created_at + ttl:
                return data
            # remove expired
            self._cache.pop(key)
        return None

    async def set_serialized(self, key: str, value: bytes, ttl_sec: int) -> None:
        # If we already have this key, remove it first
        if key in self._cache:
            self._cache.pop(key)
        # If we're at capacity, remove the lease recently used item
        if len(self._cache) >= self.max_size:
            self._cache.popitem(last=False)
        self._cache[key] = (value, time.time(), ttl_sec)

    async def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    async def try_lock(self, key: str, lock_period_sec: int) -> bool:
        # imitate simple redis lock with ttl
        lock_data = self._distributed_locks.get(key, None)
        if lock_data:
            value, created_at, ttl = lock_data
            if time.time() < created_at + ttl:
                return False
        # no lock or expired
        self._distributed_locks[key] = (b"1", time.time(), lock_period_sec)
        return True

    async def unlock(self, key: str) -> None:
        self._distributed_locks.pop(key, None)


class MemoryBackendTTL:
    """
    In-memory LRU backend with TTL
    """

    def __init__(self, max_size: int = 1000, check_interval: float = 1) -> None:
        self.max_size = max_size
        self._cache: OrderedDict[str, tuple[bytes, float, float]] = OrderedDict()
        self._check_interval = check_interval
        self.__remove_expired_stop = asyncio.Event()
        self.__remove_expired_task = None

    async def initialize(self) -> None:
        if self._check_interval:
            self.__remove_expired_stop = asyncio.Event()
            self.__remove_expired_task = asyncio.create_task(self._remove_expired())

    async def _remove_expired(self):
        while not self.__remove_expired_stop.is_set():
            for key in dict(self._cache):
                await self.get_serialized(key)
            with suppress(asyncio.TimeoutError, TimeoutError):
                await asyncio.wait_for(self.__remove_expired_stop.wait(), self._check_interval)

    async def aclose(self) -> None:
        self._cache.clear()

    async def get_serialized(self, key: str) -> bytes | None:
        if key not in self._cache:
            return None
        self._cache.move_to_end(key)
        data, created_at, ttl = self._cache[key]
        # Check if expired
        if time.time() >= created_at + ttl:
            await self.delete(key)
            return None
        return data

    async def set_serialized(self, key: str, value: bytes, ttl_sec: int) -> None:
        # If we already have this key, remove it first
        if key in self._cache:
            self._cache.pop(key)
        # If we're at capacity, remove the least recently used item
        if len(self._cache) >= self.max_size:
            self._cache.popitem(last=False)
        self._cache[key] = (value, time.time(), ttl_sec)

    async def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    async def try_lock(self, key: str, lock_period_sec: int) -> bool:
        return True

    async def unlock(self, key: str) -> None:
        return
