import pytest  # type: ignore
from asyncio import (
    Task,
    create_task,
)

from queutils import IterableQueue, QueueDone, abatch, awrap


async def _producer_int(
    Q: IterableQueue[int], n: int, finish: bool = False, wait: float = 0
) -> None:
    await Q.add_producer(N=1)
    try:
        for i in range(n):
            await Q.put(i)
    except QueueDone:
        raise ValueError("Queue is done even no one closed it")
    await Q.finish_producer()
    return None


@pytest.mark.timeout(5)
@pytest.mark.parametrize(
    "N",
    [
        (int(10e4)),
        (int(10e4)),
    ],
)
@pytest.mark.asyncio
async def test_1_awrap_iterable(N: int):
    """Test for awrap() with AsyncIterable"""

    iterable: list[int] = [i for i in range(N)]

    max_elem: int = -1

    async for elem in awrap(iterable):
        assert elem > max_elem, "outcome"
        max_elem = elem
    assert max_elem == N - 1, f"last element is incorrect: {max_elem} != {N - 1}"


@pytest.mark.timeout(5)
@pytest.mark.parametrize(
    "bsize, N",
    [
        (17, int(10e4)),
        (89, int(10e4)),
    ],
)
@pytest.mark.asyncio
async def test_2_abatch_iterable(bsize: int, N: int):
    """Test for abatch() with AsyncIterable"""

    iterable: list[int] = [i for i in range(N)]

    max_elem: int = -1
    last: bool = False

    async for batch in abatch(iterable, bsize):
        assert not last, "abatch() returned mismatched batch that was not the last"
        if len(batch) < bsize:
            last = True
        assert last or len(batch) == bsize, f"Batch size is {len(batch)} != {bsize}"
        for elem in batch:
            assert elem > max_elem, f"batch is not sorted: {batch}"
            max_elem = elem


@pytest.mark.timeout(10)
@pytest.mark.parametrize(
    "Qsize, bsize, N",
    [
        (101, 17, int(10e4)),
        (11, 89, int(10e4)),
    ],
)
@pytest.mark.asyncio
async def test_3_abatch_asynciterable(Qsize: int, bsize: int, N: int):
    """Test for abatch() with AsyncIterable"""

    Q = IterableQueue[int](maxsize=Qsize)
    producer: Task = create_task(_producer_int(Q, N))

    max_elem: int = -1
    last: bool = False

    async for batch in abatch(Q, bsize):
        assert not last, "abatch() returned mismatched batch that was not the last"
        if len(batch) < bsize:
            last = True
        assert last or len(batch) == bsize, f"Batch size is {len(batch)} != {bsize}"
        for elem in batch:
            assert elem > max_elem, f"batch is not sorted: {batch}"
            max_elem = elem
    assert Q.empty(), f"Queue is not empty after async for: Q.size={Q.qsize()}"
    assert Q.is_done, "Queue is not done"
    producer.cancel()
