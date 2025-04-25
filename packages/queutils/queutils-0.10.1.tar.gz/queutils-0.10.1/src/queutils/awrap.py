"""awrap() is a async wrapper for Iterables

It converts an Iterable[T] to AsyncGenerator[T].
AsyncGenerator[T] is also AsyncIterable[T] allowing it to be used in async for
"""

from typing import Iterable, Sequence, TypeVar, AsyncGenerator, AsyncIterable

T = TypeVar("T")


async def awrap(iterable: Iterable[T]) -> AsyncGenerator[T, None]:
    """
    Async wrapper for Iterable[T] so it can be used in async for
    Can be used in async for loop
    """
    for item in iter(iterable):
        yield item


async def abatch(
    iterable: Iterable[T] | AsyncIterable[T], size: int
) -> AsyncGenerator[Sequence[T], None]:
    """
    Async wrapper reads batches from a AsyncIterable[T] or Iterable[T]
    Can be used in async for loop
    """
    batch: list[T] = []
    if isinstance(iterable, AsyncIterable):
        async for item in iterable:
            batch.append(item)
            if len(batch) == size:
                yield batch
                batch = []
    elif isinstance(iterable, Iterable):
        for item in iterable:
            batch.append(item)
            if len(batch) == size:
                yield batch
                batch = []
    else:
        raise TypeError(f"Expected Iterable or AsyncIterable, got {type(iterable)}")

    if batch:
        yield batch
