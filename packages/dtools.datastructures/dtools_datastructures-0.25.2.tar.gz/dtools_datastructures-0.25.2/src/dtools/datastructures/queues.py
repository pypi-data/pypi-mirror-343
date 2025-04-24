# Copyright 2023-2024 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
### Queue based data structures

* stateful queue data structures with amortized O(1) pushes and pops each end
* obtaining length (number of elements) of a queue is an O(1) operation
* implemented in a "has-a" relationship with a Python list based circular array
* these data structures will resize themselves larger as needed

#### FIFOQueue

* class FIFOQueue: First-In-First-Out Queue
* function FQ: Constructs a FIFOQueue from a variable number of arguments

---

#### LIFOQueue

* class LIFOQueue: Last-In-First-Out Queue
* function LQ: Constructs a LIFOQueue from a variable number of arguments

---

#### DoubleQueue

* class DoubleQueue: Double-Ended Queue
* function DQ: Constructs a DoubleQueue from a variable number of arguments

"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Sequence
from typing import Never, overload, TypeVar
from dtools.circular_array.ca import ca, CA
from dtools.fp.err_handling import MB

__all__ = ['DoubleQueue', 'FIFOQueue', 'LIFOQueue', 'QueueBase', 'DQ', 'FQ', 'LQ']

D = TypeVar('D')  # Not needed for mypy, hint for pdoc.
L = TypeVar('L')
R = TypeVar('R')
U = TypeVar('U')


class QueueBase[D](Sequence[D]):
    """Base class for circular area based queues.

    * implemented with a dtools.circular-array in a "has-a" relationship
    * order of initial data retained
    * slicing not yet implemented

    """

    __slots__ = ('_ca',)

    def __init__(self, *dss: Iterable[D]) -> None:
        if len(dss) < 2:
            self._ca = ca(*dss)
        else:
            msg1 = f'{type(self).__name__}: expected at most 1 '
            msg2 = f'iterable argument, got {len(dss)}.'
            raise TypeError(msg1 + msg2)

    def __bool__(self) -> bool:
        return len(self._ca) > 0

    def __len__(self) -> int:
        return len(self._ca)

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._ca == other._ca

    @overload
    def __getitem__(self, idx: int, /) -> D: ...
    @overload
    def __getitem__(self, idx: slice, /) -> Sequence[D]: ...

    def __getitem__(self, idx: int | slice, /) -> D | Sequence[D] | Never:
        if isinstance(idx, slice):
            raise NotImplementedError
        return self._ca[idx]


class FIFOQueue[D](QueueBase[D]):
    """FIFO Queue

    * stateful First-In-First-Out (FIFO) data structure
    * initial data pushed on in natural FIFO order

    """

    __slots__ = ()

    def __iter__(self) -> Iterator[D]:
        return iter(list(self._ca))

    def __repr__(self) -> str:
        if len(self) == 0:
            return 'FQ()'
        else:
            return 'FQ(' + ', '.join(map(repr, self._ca)) + ')'

    def __str__(self) -> str:
        return '<< ' + ' < '.join(map(str, self)) + ' <<'

    def copy(self) -> FIFOQueue[D]:
        """Return a shallow copy of the `FIFOQueue`."""
        return FIFOQueue(self._ca)

    def push(self, *ds: D) -> None:
        """Push data onto `FIFOQueue`.

        * like a Python List, does not return a value

        """
        self._ca.pushR(*ds)

    def pop(self) -> MB[D]:
        """Pop data from `FIFOQueue`.

        * pop item off queue, return item in a maybe monad
        * returns an empty `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca.popL())
        else:
            return MB()

    def peak_last_in(self) -> MB[D]:
        """Peak last data into `FIFOQueue`.

        * return a maybe monad of the last item pushed to queue
        * does not consume the data
        * if item already popped, return `MB()`

        """
        if self._ca:
            return MB(self._ca[-1])
        else:
            return MB()

    def peak_next_out(self) -> MB[D]:
        """Peak next data out of `FIFOQueue`.

        * returns a maybe monad of the next item to be popped from the queue.
        * does not consume it the item
        * returns `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca[0])
        else:
            return MB()

    def fold[L](self, f: Callable[[L, D], L], initial: L | None = None, /) -> MB[L]:
        """Fold `FIFOQueue` in natural order.

        Reduce with `f` using an optional initial value.

        * folds in natural FIFO Order (oldest to newest)
        * note that when an initial value is not given then `~L = ~D`
        * if iterable empty & no initial value given, return `MB()`
        * traditional FP type order given for function `f`

        """
        if initial is None:
            if not self._ca:
                return MB()
        return MB(self._ca.foldL(f, initial=initial))

    def map[U](self, f: Callable[[D], U], /) -> FIFOQueue[U]:
        """Map over the `FIFOQueue`.

        * map function `f` over the queue
          * oldest to newest
          * retain original order
        * returns a new instance

        """
        return FIFOQueue(map(f, self._ca))


class LIFOQueue[D](QueueBase[D]):
    """LIFO Queue.

    * stateful Last-In-First-Out (LIFO) data structure
    * initial data pushed on in natural LIFO order

    """

    __slots__ = ()

    def __iter__(self) -> Iterator[D]:
        return reversed(list(self._ca))

    def __repr__(self) -> str:
        if len(self) == 0:
            return 'LQ()'
        return 'LQ(' + ', '.join(map(repr, self._ca)) + ')'

    def __str__(self) -> str:
        return '|| ' + ' > '.join(map(str, self)) + ' ><'

    def copy(self) -> LIFOQueue[D]:
        """Return a shallow copy of the `LIFOQueue`."""
        return LIFOQueue(reversed(self._ca))

    def push(self, *ds: D) -> None:
        """Push data onto `LIFOQueue`.

        * like a Python List, does not return a value

        """
        self._ca.pushR(*ds)

    def pop(self) -> MB[D]:
        """Pop data from `LIFOQueue`.

        * pop item off of queue, return item in a maybe monad
        * returns an empty `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca.popR())
        return MB()

    def peak(self) -> MB[D]:
        """Peak next data out of `LIFOQueue`.

        * return a maybe monad of the next item to be popped from the queue
        * does not consume the item
        * returns `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca[-1])
        return MB()

    def fold[R](self, f: Callable[[D, R], R], initial: R | None = None, /) -> MB[R]:
        """Fold `LIFOQueue` in natural order.

        Reduce with `f` using an optional initial value.

        * folds in natural LIFO Order (newest to oldest)
        * note that when an initial value is not given then `~R = ~D`
        * if iterable empty & no initial value given, return `MB()`
        * traditional FP type order given for function `f`

        """
        if initial is None:
            if not self._ca:
                return MB()
        return MB(self._ca.foldR(f, initial=initial))

    def map[U](self, f: Callable[[D], U], /) -> LIFOQueue[U]:
        """Map Over the `LIFOQueue`.

        * map the function `f` over the queue
          * newest to oldest
          * retain original order
        * returns a new instance

        """
        return LIFOQueue(reversed(CA(*map(f, reversed(self._ca)))))


class DoubleQueue[D](QueueBase[D]):
    """Double Ended Queue

    * stateful Double-Ended (DEQueue) data structure
    * order of initial data retained

    """

    __slots__ = ()

    def __iter__(self) -> Iterator[D]:
        return iter(list(self._ca))

    def __reversed__(self) -> Iterator[D]:
        return reversed(list(self._ca))

    def __repr__(self) -> str:
        if len(self) == 0:
            return 'DQ()'
        return 'DQ(' + ', '.join(map(repr, self._ca)) + ')'

    def __str__(self) -> str:
        return '>< ' + ' | '.join(map(str, self)) + ' ><'

    def copy(self) -> DoubleQueue[D]:
        """Return a shallow copy of the `DoubleQueue`."""
        return DoubleQueue(self._ca)

    def pushL(self, *ds: D) -> None:
        """Push data onto left side (front) of `DoubleQueue`.

        * like a Python List, does not return a value

        """
        self._ca.pushL(*ds)

    def pushR(self, *ds: D) -> None:
        """Push data onto right side (rear) of `DoubleQueue`.

        * like a Python List, does not return a value

        """
        self._ca.pushR(*ds)

    def popL(self) -> MB[D]:
        """Pop Data from left side (front) of `DoubleQueue`.

        * pop left most item off of queue, return item in a maybe monad
        * returns an empty `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca.popL())
        else:
            return MB()

    def popR(self) -> MB[D]:
        """Pop Data from right side (rear) of `DoubleQueue`.

        * pop right most item off of queue, return item in a maybe monad
        * returns an empty `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca.popR())
        return MB()

    def peakL(self) -> MB[D]:
        """Peak left side of `DoubleQueue`.

        * return left most value in a maybe monad
        * does not consume the item
        * returns an empty `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca[0])
        return MB()

    def peakR(self) -> MB[D]:
        """Peak right side of `DoubleQueue`.

        * return right most value in a maybe monad
        * does not consume the item
        * returns an empty `MB()` if queue is empty

        """
        if self._ca:
            return MB(self._ca[-1])
        return MB()

    def foldL[L](self, f: Callable[[L, D], L], initial: L | None = None, /) -> MB[L]:
        """Fold `DoubleQueue` left to right.

        Reduce left with `f` using an optional initial value.

        * note that when an initial value is not given then `~L = ~D`
        * if iterable empty & no initial value given, return `MB()`
        * traditional FP type order given for function `f`

        """
        if initial is None:
            if not self._ca:
                return MB()
        return MB(self._ca.foldL(f, initial=initial))

    def foldR[R](self, f: Callable[[D, R], R], initial: R | None = None, /) -> MB[R]:
        """Fold `DoubleQueue` right to left.

        Reduce right with `f` using an optional initial value.

        * note that when an initial value is not given then `~R = ~D`
        * if iterable empty & no initial value given, return `MB()`
        * traditional FP type order given for function `f`

        """
        if initial is None:
            if not self._ca:
                return MB()
        return MB(self._ca.foldR(f, initial=initial))

    def map[U](self, f: Callable[[D], U], /) -> DoubleQueue[U]:
        """`Map a function over `DoubleQueue`.

        * map the function `f` over the `DoubleQueue`
          * left to right
          * retain original order
        * returns a new instance

        """
        return DoubleQueue(map(f, self._ca))


def FQ[D](*ds: D) -> FIFOQueue[D]:
    """Return a FIFOQueue where data is pushed on in natural FIFO order."""
    return FIFOQueue(ds)


def LQ[D](*ds: D) -> LIFOQueue[D]:
    """Return a LIFOQueue where data is pushed on in natural LIFO order."""
    return LIFOQueue(ds)


def DQ[D](*ds: D) -> DoubleQueue[D]:
    """Return a DoubleQueue whose data is pushed on from the right."""
    return DoubleQueue(ds)
