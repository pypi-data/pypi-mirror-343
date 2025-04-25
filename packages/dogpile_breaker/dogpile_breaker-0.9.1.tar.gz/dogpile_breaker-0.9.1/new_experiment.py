import asyncio
from datetime import datetime, timezone
from typing import Callable, Awaitable

from dogpile_breaker.middlewares.circut_breaker_fallback_middleware import CircuitBreakerFallbackMiddleware
from dogpile_breaker.middlewares.fallback_middleware import FallbackMiddleware
from dogpile_breaker.backends.redis_backend import RedisStorageBackend
from dogpile_breaker.backends.memory_backend import MemoryBackendLRU
from dogpile_breaker.api import CacheRegion
import orjson

from dogpile_breaker.middlewares.prometheus_middleware import PrometheusMiddleware


def my_serializer(data: str) -> bytes:
    return data.encode("utf-8")


def my_deserializer(data: bytes) -> str:
    return data.decode("utf-8")


def cache_key_generator(fn: Callable[[int], Awaitable[str]], sleep_for: int) -> str:
    """
    This function are going to be called with the source function and all the args & kwargs of a call.
    It should return string used as a key in cache to store result.
    """
    return f"{fn.__name__}:{sleep_for}"


async def expensive_func(sleep_for: int) -> str:
    print(f"{datetime.now(tz=timezone.utc)} | Running expensive_func")
    await asyncio.sleep(sleep_for)
    return f"This is result for parameter {sleep_for=}"


async def main():
    cache_instance = CacheRegion(
        serializer=my_serializer,
        deserializer=my_deserializer,
    )
    memory_backend = MemoryBackendLRU()
    cb_middleware = CircuitBreakerFallbackMiddleware(
        fallback_storage=memory_backend,
    )
    await cache_instance.configure(
        backend_class=RedisStorageBackend,
        backend_arguments={
            "host": "localhost",
            "port": 6379,
            "db": 0,
        },
        middlewares=[cb_middleware, PrometheusMiddleware(region_name="articles-cache")],
    )
    while True:
        await asyncio.sleep(1)
        result = await cache_instance.get_or_create(
            key="expensive_func_1",
            ttl_sec=5,
            lock_period_sec=2,
            generate_func=expensive_func,
            generate_func_args=(),
            generate_func_kwargs={"sleep_for": 1},
        )
        print(f"{datetime.now(tz=timezone.utc)} | Function result: {result=}")


if __name__ == "__main__":
    asyncio.run(main())
