from dogpile_breaker.backends.memory_backend import MemoryBackendLRU


async def main():
    mb = MemoryBackendLRU()
    await mb.initialize()
