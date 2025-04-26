import asyncio


async def maybe_coro(func, *args, **kwargs):
    """Call the given func, awaiting if required.

    Args and Kwargs are passed directly to the coroutine.
    """
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)

    return func(*args, **kwargs)
