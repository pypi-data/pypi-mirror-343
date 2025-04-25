# -----------------------------------------------------------
#  Class IterableQueue(asyncio.Queue[T], AsyncIterable[T], Countable)
#
#  IterableQueue is asyncio.Queue subclass that can be iterated asynchronusly.
#  IterableQueue terminates automatically when the queue has been
#  filled and emptied.
#
# -----------------------------------------------------------

__author__ = "Jylpah"
__copyright__ = "Copyright 2024, Jylpah <Jylpah@gmail.com>"
__credits__ = ["Jylpah"]
__license__ = "MIT"
# __version__ = "1.0"
__maintainer__ = "Jylpah"
__email__ = "Jylpah@gmail.com"
__status__ = "Production"


from asyncio import Queue, QueueFull, Event, Lock
from typing import AsyncIterable, TypeVar, Optional
from deprecated import deprecated
from .countable import Countable
import logging

# Setup logging
logger = logging.getLogger(__name__)
debug = logger.debug

T = TypeVar("T")


class QueueDone(Exception):
    """
    Exception to mark an IterableQueue as filled and emptied i.e. done
    """

    pass


class IterableQueue(Queue[T], AsyncIterable[T], Countable):
    """
    IterableQueue is asyncio.Queue subclass that can be iterated asynchronusly.

    IterableQueue terminates automatically when the queue has been
    filled and emptied.

    Supports:
    - asyncio.Queue() interface, _nowait() methods are experimental
    - AsyncIterable(): async for item in queue:
    - Automatic termination of the consumers when the queue has been emptied with QueueDone exception
    - Producers must be registered with add_producer() and they must notify the queue
      with finish_producer() once they have finished adding items
    - Countable interface to count number of items task_done() through 'count' property

    IterableQueue stages:

    1) Initialized: Queue has been created and it is empty
    2) is_illed: All producers have finished adding items to the queue
    3) empty/has_wip: Queue has been emptied
    4) is_done: All items have been marked with task_done()
    """

    def __init__(self, **kwargs) -> None:
        # _Q is required instead of inheriting from Queue()
        # using super() since Queue is Optional[T], not [T]
        self._Q: Queue[Optional[T]] = Queue(**kwargs)
        self._maxsize: int = self._Q.maxsize  # Asyncio.Queue has _maxsize
        self._producers: int = 0
        self._count: int = 0
        self._wip: int = 0

        self._modify: Lock = Lock()
        self._put_lock: Lock = Lock()

        # the last producer has finished
        self._filled: Event = Event()
        # the last producer has finished and the queue is empty
        self._empty: Event = Event()
        # the queue is done, all items have been marked with task_done()
        self._done: Event = Event()

        self._empty.clear()  # this will be tested only after queue is filled

    @property
    def is_filled(self) -> bool:
        """ "
        True if all the producers finished filling the queue.
        New items cannot be added to a filled queue nor can new producers can be added.
        """
        return self._filled.is_set()

    @property
    def is_done(self) -> bool:
        """
        Has the queue been filled, emptied and all the items have been marked with task_done()
        """
        return self.is_filled and self.empty() and not self.has_wip

    @property
    def maxsize(self) -> int:
        return self._Q.maxsize

    def full(self) -> bool:
        """
        True if the queue is full
        """
        return self._Q.full()

    def empty(self) -> bool:
        """
        Queue has no items except None as a sentinel
        """
        return self._empty.is_set() or self.qsize() == 0

    def qsize(self) -> int:
        """
        asyncio.Queue.qsize()
        """
        if self.is_filled:
            return self._Q.qsize() - 1
        else:
            return self._Q.qsize()

    @property
    def wip(self) -> int:
        """
        Number of items in progress i.e. items that have been
        read from the queue, but not marked with task_done()
        """
        return self._wip

    @property
    def has_wip(self) -> bool:
        """
        True if queue has items in progress
        """
        return self._wip > 0

    @property
    def count(self) -> int:
        return self._count

    async def add_producer(self, N: int = 1) -> int:
        """
        Add producer(s) to the queue
        """
        if N <= 0:
            raise ValueError("N has to be positive")
        async with self._modify:
            if self.is_filled:
                raise QueueDone
            self._producers += N
        return self._producers

    @deprecated(version="0.10.0", reason="Use finish_producer() instead for clarity")
    async def finish(self, all: bool = False) -> bool:
        """
        Finish producer

        Depreciated function, use finish_producer() instead
        """
        return await self.finish_producer(all=all)

    async def finish_producer(self, all: bool = False) -> bool:
        """
        Producer has finished adding items to the queue.
        Once the last producers has finished, the queue is_filled.
        - all: finish_producer() queue for all producers at once

        Return True if the last producer is 'finished'
        """
        async with self._modify:
            if self.is_filled:
                return True

            self._producers -= 1

            if self._producers < 0:
                raise ValueError("Too many finish_producer() calls")
            elif all or self._producers == 0:
                self._filled.set()
                self._producers = 0

        if self._producers == 0:
            async with self._put_lock:
                if self._Q.qsize() == 0:
                    self._empty.set()
                    if not self.has_wip:
                        self._done.set()
                await self._Q.put(None)
                return True
        return False

    async def put(self, item: T) -> None:
        if item is None:
            raise ValueError("Cannot add None to IterableQueue")
        async with self._put_lock:
            if self.is_filled:  # should this be inside put_lock?
                raise QueueDone
            if self._producers <= 0:
                raise ValueError("No registered producers")
            await self._Q.put(item=item)
        return None

    def put_nowait(self, item: T) -> None:
        """
        Experimental asyncio.Queue.put_nowait() implementation
        """
        if self.is_filled:
            raise QueueDone
        if self._producers <= 0:
            raise ValueError("No registered producers")
        if item is None:
            raise ValueError("Cannot add None to IterableQueue")
        self._Q.put_nowait(item=item)
        return None

    async def get(self) -> T:
        item = await self._Q.get()
        if item is None:
            self._empty.set()
            if not self.has_wip:
                self._done.set()
            self._Q.task_done()
            async with self._put_lock:
                await self._Q.put(None)
                raise QueueDone
        else:
            self._wip += 1
            return item

    def get_nowait(self) -> T:
        """
        Experimental asyncio.Queue.get_nowait() implementation
        """
        item: T | None = self._Q.get_nowait()
        if item is None:
            self._empty.set()
            if not self.has_wip:
                self._done.set()
            self._Q.task_done()
            try:
                self._Q.put_nowait(None)
            except QueueFull:
                pass
            raise QueueDone
        else:
            self._wip += 1
            return item

    def task_done(self) -> None:
        self._Q.task_done()
        self._count += 1
        self._wip -= 1
        if self._wip < 0:
            raise ValueError("task_done() called more than tasks open")
        if self.is_filled and self._empty.is_set() and not self.has_wip:
            self._done.set()

    async def join(self) -> None:
        debug("Waiting queue to be filled")
        await self._filled.wait()
        debug("Queue filled, waiting when queue is done")
        await self._done.wait()
        debug("queue is done")
        return None

    def __aiter__(self):
        """
        Return ASyncIterator to be able iterate the queue using async for
        """
        return self

    async def __anext__(self) -> T:
        """
        Async iterator for IterableQueue
        """
        if self._wip > 0:  # do not mark task_done() at first call
            self.task_done()
        try:
            return await self.get()
        except QueueDone:
            raise StopAsyncIteration
