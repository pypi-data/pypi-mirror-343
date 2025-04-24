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

from __future__ import annotations
from typing import Optional
from dtools.circular_array.ca import CA
from dtools.datastructures.queues import DoubleQueue, DQ
from dtools.datastructures.queues import FIFOQueue, FQ
from dtools.datastructures.queues import LIFOQueue, LQ
from dtools.datastructures.tuples import FT
from dtools.fp.err_handling import MB

class TestQueueTypes:
    def test_mutate_map(self) -> None:
        dq1: DoubleQueue[int] = DQ()
        dq1.pushL(1,2,3)
        dq1.pushR(1,2,3)
        dq2 = dq1.map(lambda x: x-1)
        assert dq2.popL() == dq2.popR() == MB(2)

        def add_one_if_int(x: int|str) -> int|str:
            if type(x) == int:
                return x+1
            else:
                return x

        fq1: FIFOQueue[int] = FQ()
        fq1.push(1,2,3)
        fq1.push(4,5,6)
        fq2 = fq1.map(lambda x: x+1)
        not_none = fq2.pop()
        assert not_none != MB()
        assert not_none == MB(2)
        assert fq2.peak_last_in() == MB(7) != MB()
        assert fq2.peak_next_out() == MB(3)

        lq1: LIFOQueue[MB[int]] = LQ()  # not really a canonical way to use MB
        lq1.push(MB(1), MB(2), MB(3))
        lq1.push(MB(4), MB(), MB(5))
        lq2 = lq1.map(lambda mb: mb.bind(lambda n: MB(2*n)))
        last = lq2.pop()
        assert last.get(42) == 10
        pop_out = lq2.pop()
        assert pop_out == MB(MB()) == MB()
        assert pop_out.get(42) == 42
        assert lq2.peak() == MB(MB(8)) == MB(8)
        assert lq2.peak().get(MB(3)) == 8
        assert lq2.peak().get(3) == 8

    def test_push_then_pop(self) -> None:
        dq1 = DoubleQueue[int]()
        pushed_1 = 42
        dq1.pushL(pushed_1)
        popped_1 = dq1.popL()
        assert MB(pushed_1) == popped_1
        assert len(dq1) == 0
        pushed_1 = 0
        dq1.pushL(pushed_1)
        popped_1 = dq1.popR()
        assert pushed_1 == popped_1.get(-1) == 0
        assert not dq1
        pushed_1 = 0
        dq1.pushR(pushed_1)
        popped_2 = dq1.popL().get(1000)
        assert popped_2 != 1000
        assert pushed_1 == popped_2
        assert len(dq1) == 0

        dq2: DoubleQueue[str] = DQ()
        pushed_3 = ''
        dq2.pushR(pushed_3)
        popped_3 = dq2.popR().get('hello world')
        assert pushed_3 == popped_3
        assert len(dq2) == 0
        dq2.pushR('first')
        dq2.pushR('second')
        dq2.pushR('last')
        assert dq2.popL() == MB('first')
        assert dq2.popR() == MB('last')
        assert dq2
        dq2.popL()
        assert len(dq2) == 0

        fq: FIFOQueue[MB[int|str]] = FQ()
        fq.push(MB(42))
        fq.push(MB('bar'))
        assert fq.pop().get() == 42
        assert fq.pop().get('foo') == 'bar'  # correct execution but
        assert fq.pop().get('foo') == 'foo'  # type hints are off
        assert len(fq) == 0
        fq.push(MB(0))
        assert fq.pop() == MB(0)
        assert not fq
        assert fq.pop() == MB()
        assert len(fq) == 0
        val: MB[int|str] = MB('Bob' + 'by')
        fq.push(val)
        assert fq
        assert val.get('Robert') == fq.pop().get('Bob') == 'Bobby'
        assert len(fq) == 0
        assert fq.pop().get('Robert') == 'Robert'
        fq.push(MB('first'))
        fq.push(MB('second'))
        fq.push(MB('last'))
        poppedMB = fq.pop()
        if poppedMB == MB():
            assert False
        else:
            assert poppedMB.get('impossible') == 'first'
        assert fq.pop().get(MB()) == 'second'
        assert fq
        fq.pop()
        assert len(fq) == 0
        assert not fq

        lq: LIFOQueue[MB[int|str]] = LQ()
        lq.push(MB(42))
        lq.push(MB('bar'))
        assert lq.pop().get('foo') == 'bar'
        assert lq.pop().get('foo') == 42
        assert lq.pop().get('foo') == 'foo'
        assert len(lq) == 0
        lq.push(MB(0))
        assert lq.pop() == MB(0)
        assert not lq
        assert lq.pop() == MB()
        assert len(lq) == 0
        val2: MB[int|str] = MB('Bob' + 'by')
        lq.push(val)
        assert lq
        assert val2.get('Robert') == lq.pop().get('Bob') == 'Bobby'
        assert len(lq) == 0
        assert lq.pop().get('Robert') == 'Robert'
        lq.push(MB('first'))
        lq.push(MB('second'))
        lq.push(MB('last'))
        poppedMB = lq.pop()
        if poppedMB == MB():
            assert False
        else:
            assert poppedMB.get() == 'last'
        assert lq.pop().get(MB('impossible')) == 'second'  # the type hits are not exposing
        assert lq.pop().get('impossible') == 'first'       # the self flattening nature of MB
        assert len(lq) == 0
        assert not lq

        def is42(ii: int) -> Optional[int]:
            return None if ii == 42 else ii

        fq1: FIFOQueue[object] = FQ()
        fq2: FIFOQueue[object] = FQ()
        fq1.push(None)
        fq2.push(None)
        assert fq1 == fq2
        assert len(fq1) == 1

        barNone: tuple[int|None, ...] = (None, 1, 2, 3, None)
        bar42 = (42, 1, 2, 3, 42)
        fq3: FIFOQueue[object] = FIFOQueue(barNone)
        fq4: FIFOQueue[object] = FIFOQueue(map(is42, bar42))
        assert fq3 == fq4

        lq1: LIFOQueue[Optional[int]] = LQ()
        lq2: LIFOQueue[Optional[int]] = LQ()
        lq1.push(None, 1, 2, None)
        lq2.push(None, 1, 2, None)
        assert lq1 == lq2
        assert len(lq1) == 4

        barNone = (None, 1, 2, None, 3)
        bar42 = (42, 1, 2, 42, 3)
        lq3: LIFOQueue[Optional[int]] = LIFOQueue(barNone)
        lq4: LIFOQueue[Optional[int]] = LIFOQueue(map(is42, bar42))
        assert lq3 == lq4


    def test_pushing_None(self) -> None:
        dq1: DoubleQueue[Optional[int]] = DoubleQueue()
        dq2: DoubleQueue[Optional[int]] = DoubleQueue()
        dq1.pushR(None)
        dq2.pushL(None)
        assert dq1 == dq2

        def is42(ii: int) -> Optional[int]:
            return None if ii == 42 else ii

        barNone = (1, 2, None, 3, None, 4)
        bar42 = (1, 2, 42, 3, 42, 4)
        dq3 = DoubleQueue[Optional[int]](barNone)
        dq4 = DoubleQueue[Optional[int]](map(is42, bar42))
        assert dq3 == dq4

    def test_bool_len_peak(self) -> None:
        dq: DoubleQueue[int] = DQ()
        assert not dq
        dq.pushL(2,1)
        dq.pushR(3)
        assert dq
        assert len(dq) == 3
        assert dq.popL() == MB(1)
        assert len(dq) == 2
        assert dq
        assert dq.peakL() == MB(2)
        assert dq.peakR() == MB(3)
        assert dq.popR() == MB(3)
        assert len(dq) == 1
        assert dq
        assert dq.popL() == MB(2)
        assert len(dq) == 0
        assert not dq
        assert len(dq) == 0
        assert not dq
        dq.pushR(42)
        assert len(dq) == 1
        assert dq
        assert dq.peakL() == MB(42)
        assert dq.peakR() == MB(42)
        assert dq.popR() == MB(42)
        assert not dq
        assert dq.peakL() == MB()
        assert dq.peakR() == MB()

        fq: FIFOQueue[int] = FQ()
        assert not fq
        fq.push(1,2,3)
        assert fq
        assert fq.peak_next_out() == MB(1)
        assert fq.peak_last_in() == MB(3)
        assert len(fq) == 3
        assert fq.pop() == MB(1)
        assert len(fq) == 2
        assert fq
        assert fq.pop() == MB(2)
        assert len(fq) == 1
        assert fq
        assert fq.pop() == MB(3)
        assert len(fq) == 0
        assert not fq
        assert fq.pop().get(-42) == -42
        assert len(fq) == 0
        assert not fq
        fq.push(42)
        assert fq
        assert fq.peak_next_out() == MB(42)
        assert fq.peak_last_in() == MB(42)
        assert len(fq) == 1
        assert fq
        assert fq.pop() == MB(42)
        assert not fq
        assert fq.peak_next_out().get(-42) == -42
        assert fq.peak_last_in().get(-42) == -42

        lq: LIFOQueue[int] = LQ()
        assert not lq
        lq.push(1,2,3)
        assert lq
        assert lq.peak() == MB(3)
        assert len(lq) == 3
        assert lq.pop() == MB(3)
        assert len(lq) == 2
        assert lq
        assert lq.pop() == MB(2)
        assert len(lq) == 1
        assert lq
        assert lq.pop() == MB(1)
        assert len(lq) == 0
        assert not lq
        assert lq.pop() == MB()
        assert len(lq) == 0
        assert not lq
        lq.push(42)
        assert lq
        assert lq.peak() == MB(42)
        assert len(lq) == 1
        assert lq
        lq.push(0)
        assert lq.peak() == MB(0)
        popped = lq.pop()
        assert popped.get(-1) == 0
        assert lq.peak() == MB(42)
        popped2 = lq.pop().get(-1)
        assert popped2 == 42
        assert not lq
        assert lq.peak() == MB()
        assert lq.pop() == MB()

    def test_iterators(self) -> None:
        data_d = FT(1, 2, 3, 4, 5)
        data_mb = data_d.map(lambda d: MB(d))
        dq: DoubleQueue[MB[int]] = DoubleQueue(data_mb)
        ii = 0
        for item in dq:
            assert data_mb[ii] == item
            ii += 1
        assert ii == 5

        dq0: DoubleQueue[bool] = DQ()
        for _ in dq0:
            assert False

        data_bool_mb: tuple[MB[bool], ...] = ()
        dq1: DoubleQueue[MB[bool]] = DoubleQueue(data_bool_mb)
        for _ in dq1:
            assert False
        dq1.pushR(MB(True))
        dq1.pushL(MB(True))
        dq1.pushR(MB(True))
        dq1.pushL(MB(False))
        assert not dq1.popL().get(True)
        while dq1:
            assert dq1.popL().get(False)
        assert dq1.popR() == MB()

        def wrapMB(x: int) -> MB[int]:
            return MB(x)

        data_ca = CA(1, 2, 3, 4, 0, 6, 7, 8, 9)
        fq: FIFOQueue[MB[int]] = FIFOQueue(data_ca.map(wrapMB))
        assert data_ca[0] == 1
        assert data_ca[-1] == 9
        ii = 0
        for item in fq:
            assert data_ca[ii] == item.get()
            ii += 1
        assert ii == 9

        fq0: FIFOQueue[MB[int]] = FQ()
        for _ in fq0:
            assert False

        fq00: FIFOQueue[int] = FQ(*())
        for _ in fq00:
            assert False
        assert not fq00

        data_list: list[int] = list(range(1,1001))
        lq: LIFOQueue[int] = LIFOQueue(data_list)
        ii = len(data_list) - 1
        for item_int in lq:
            assert data_list[ii] == item_int
            ii -= 1
        assert ii == -1

        lq0: LIFOQueue[int] = LQ()
        for _ in lq0:
            assert False
        assert not lq0
        assert lq0.pop() == MB()

        lq00: LIFOQueue[int] = LQ(*())
        for _ in lq00:
            assert False
        assert not lq00
        assert lq00.pop() == MB()

    def test_equality(self) -> None:
        dq1: DoubleQueue[object] = DQ(1, 2, 3, 'Forty-Two', (7, 11, 'foobar'))
        dq2: DoubleQueue[object] = DQ(2, 3, 'Forty-Two')
        dq2.pushL(1)
        dq2.pushR((7, 11, 'foobar'))
        assert dq1 == dq2

        tup = dq2.popR().get(tuple(range(42)))
        assert dq1 != dq2

        dq2.pushR((42, 'foofoo'))
        assert dq1 != dq2

        dq1.popR()
        dq1.pushR((42, 'foofoo'))
        dq1.pushR(tup)
        dq2.pushR(tup)
        assert dq1 == dq2

        holdA = dq1.popL().get(0)
        holdB = dq1.popL().get(0)
        holdC = dq1.popR().get(0)
        dq1.pushL(holdB)
        dq1.pushR(holdC)
        dq1.pushL(holdA)
        dq1.pushL(200)
        dq2.pushL(200)
        assert dq1 == dq2

        tup1 = 7, 11, 'foobar'
        tup2 = 42, 'foofoo'

        fq1 = FQ(1, 2, 3, 'Forty-Two', tup1)
        fq2 = FQ(2, 3, 'Forty-Two')
        fq2.push((7, 11, 'foobar'))
        popped = fq1.pop()
        assert popped == MB(1)
        assert fq1 == fq2

        fq2.push(tup2)
        assert fq1 != fq2

        fq1.push(fq1.pop(), fq1.pop(), fq1.pop())
        fq2.push(fq2.pop(), fq2.pop(), fq2.pop())
        fq2.pop()
        assert MB(tup2) == fq2.peak_next_out()
        assert fq1 != fq2
        assert fq1.pop() != fq2.pop()
        assert fq1 == fq2
        fq1.pop()
        assert fq1 != fq2
        fq2.pop()
        assert fq1 == fq2

        l1 = ['foofoo', 7, 11]
        l2 = ['foofoo', 42]

        lq1: LIFOQueue[object] = LQ(3, 'Forty-Two', l1, 1)
        lq2: LIFOQueue[object] = LQ(3, 'Forty-Two', 2)
        assert lq1.pop() == MB(1)
        peak = lq1.peak().get([1,2,3,4,5])
        assert peak == l1
        assert type(peak) == list
        assert peak.pop() == 11
        assert peak.pop() == 7
        peak.append(42)
        assert lq2.pop() == MB(2)
        lq2.push(l2)
        assert lq1 == lq2

        lq2.push(42)
        assert lq1 != lq2

        lq3: LIFOQueue[str] = LIFOQueue(map(lambda i: str(i), range(43)))
        lq4: LIFOQueue[int] = LQ(*range(-1, 39), 41, 40, 39)

        lq3.push(lq3.pop().get(), lq3.pop().get(), lq3.pop().get())
        lq5 = lq4.map(lambda i: str(i+1))
        assert lq3 == lq5

    def test_map(self) -> None:
        def f1(ii: int) -> int:
            return ii*ii - 1

        def f2(ii: int) -> str:
            return str(ii)

        dq = DQ(5, 2, 3, 1, 42)
        dq0: DoubleQueue[int] = DQ()
        dq1 = dq.copy()
        assert dq1 == dq
        assert dq1 is not dq
        dq0m = dq0.map(f1)
        dq1m = dq1.map(f1)
        assert dq == DQ(5, 2, 3, 1, 42)
        assert dq0m == DQ()
        assert dq1m == DQ(24, 3, 8, 0, 1763)
        assert dq0m.map(f2) == DQ()
        assert dq1m.map(f2) == DQ('24', '3', '8', '0', '1763')

        fq0: FIFOQueue[int] = FQ()
        fq1: FIFOQueue[int] = FQ(5, 42, 3, 1, 2)
        q0m = fq0.map(f1)
        q1m = fq1.map(f1)
        assert q0m == FQ()
        assert q1m == FQ(24, 1763, 8, 0, 3)

        fq0.push(8, 9, 10)
        assert fq0.pop().get(-1) == 8
        assert fq0.pop() == MB(9)
        fq2 = fq0.map(f1)
        assert fq2 == FQ(99)
        assert fq2 == FQ(99)

        fq2.push(100)
        fq3 = fq2.map(f2)
        assert fq3 == FQ('99', '100')

        lq0: LIFOQueue[int] = LQ()
        lq1 = LQ(5, 42, 3, 1, 2)
        lq0m = lq0.map(f1)
        lq1m = lq1.map(f1)
        assert lq0m == LQ()
        assert lq1m == LQ(24, 1763, 8, 0, 3)

        lq0.push(8, 9, 10)
        assert lq0.pop() == MB(10)
        assert lq0.pop() == MB(9)
        lq2 = lq0.map(f1)
        assert lq2 == LQ(63)

        lq2.push(42)
        lq3 = lq2.map(f2)
        assert lq3 == LQ('63', '42')
