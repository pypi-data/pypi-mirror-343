import typing
from typing import Self

from dogpile_breaker.exceptions import CacheBackendInteractionError
from dogpile_breaker.middlewares.base_middleware import StorageBackendMiddleware

if typing.TYPE_CHECKING:
    from dogpile_breaker.api import StorageBackend


class FallbackMiddleware(StorageBackendMiddleware):
    """
    Try proxied ops first.

    On any CacheBackendInteractionError delegate to the provided in-memory backend.
    """

    def __init__(self, fallback: "StorageBackend") -> None:
        self._fallback = fallback

    # def wrap(self, backend_storage: "StorageBackend") -> Self:
    #     self._original_backend = backend_storage
    #     return self

    async def initialize(self) -> None:
        await self.proxied.initialize()
        await self._fallback.initialize()

    async def aclose(self) -> None:
        await self.proxied.aclose()
        await self._fallback.aclose()

    async def get_serialized(self, key: str) -> bytes | None:
        try:
            return await self.proxied.get_serialized(key)
        except CacheBackendInteractionError:
            return await self._fallback.get_serialized(key)

    async def set_serialized(self, key: str, value: bytes, ttl_sec: int) -> None:
        try:
            await self.proxied.set_serialized(key, value, ttl_sec)
        except CacheBackendInteractionError:
            await self._fallback.set_serialized(key, value, ttl_sec)

    async def try_lock(self, key: str, lock_period_sec: int) -> bool:
        try:
            return await self.proxied.try_lock(key, lock_period_sec)
        except CacheBackendInteractionError:
            return await self._fallback.try_lock(key, lock_period_sec)

    async def unlock(self, key: str) -> None:
        try:
            await self.proxied.unlock(key)
        except CacheBackendInteractionError:
            await self._fallback.unlock(key)
