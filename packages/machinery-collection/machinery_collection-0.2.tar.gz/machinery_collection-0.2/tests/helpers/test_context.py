import asyncio
import contextlib
import dataclasses
import logging
import sys
import time
import types
from collections.abc import AsyncGenerator, Callable, Iterator

import pytest
import pytest_subtests

from machinery import helpers as hp
from machinery import test_helpers as thp
from machinery._helpers import _context


@pytest.fixture
def log() -> logging.Logger:
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    return log


@pytest.fixture
def ctx(log: logging.Logger) -> Iterator[hp.CTX]:
    tramp: hp.protocols.Tramp = hp.Tramp(log=log)
    with hp.CTX.beginning(name="::", tramp=tramp) as ctx:
        yield ctx


@dataclasses.dataclass(frozen=True)
class CalledHelper:
    _called: list[int | str] = dataclasses.field(default_factory=list)

    def make_on_done(
        self,
        event: asyncio.Event,
        expected_ctx: hp.protocols.CTX,
        value: int | str,
        expected_exception: type[asyncio.CancelledError] | Exception | None,
    ) -> hp.protocols.FutureCTXCallback[None]:
        def on_done(ctx: hp.protocols.CTX, res: hp.protocols.FutureStatus[None]) -> None:
            event.set()
            assert ctx is expected_ctx

            if expected_exception is None:
                assert res.done() and not res.cancelled() and res.exception() is None
            elif expected_exception is asyncio.CancelledError:
                assert res.done() and res.cancelled()
            else:
                assert res.done() and res.exception() == expected_exception

            self._called.append(value)

        return on_done

    def make_simpler_on_done(
        self,
        event: asyncio.Event,
        value: int | str,
        expected_exception: type[asyncio.CancelledError] | Exception | None,
    ) -> hp.protocols.FutureCallback[None]:
        def on_done(res: hp.protocols.FutureStatus[None]) -> None:
            event.set()

            if expected_exception is None:
                assert res.done() and not res.cancelled() and res.exception() is None
            elif expected_exception is asyncio.CancelledError:
                assert res.done() and res.cancelled()
            else:
                assert res.done() and res.exception() == expected_exception

            self._called.append(value)

        return on_done

    def __eq__(self, o: object) -> bool:
        return self._called == o

    def append(self, value: int | str) -> None:
        self._called.append(value)

    def clear(self) -> None:
        self._called.clear()

    def __repr__(self) -> str:
        return f"CH[{self._called}]"


class TestTramp:
    class TestFutureNames:
        def test_can_set_and_get_names_for_futures(
            self, log: logging.Logger, loop: asyncio.AbstractEventLoop
        ) -> None:
            fut: asyncio.Future[None] = loop.create_future()
            tramp = hp.Tramp(log=log)

            assert tramp.get_future_name(fut) is None

            tramp.set_future_name(fut, name="hello")
            assert tramp.get_future_name(fut) == "hello"

            fut2: asyncio.Future[None] = loop.create_future()
            assert tramp.get_future_name(fut2) is None
            assert tramp.get_future_name(fut) == "hello"

            tramp.set_future_name(fut, name="hi")
            assert tramp.get_future_name(fut2) is None
            assert tramp.get_future_name(fut) == "hi"

            tramp.set_future_name(fut2, name="there")
            assert tramp.get_future_name(fut2) == "there"
            assert tramp.get_future_name(fut) == "hi"

            assert _context.get_fut_names() == {fut: "hi", fut2: "there"}
            del fut
            assert _context.get_fut_names() == {fut2: "there"}

    class TestFutureToString:
        @pytest.fixture
        def tramp(self, log: logging.Logger) -> hp.Tramp:
            return hp.Tramp(log=log)

        def test_just_reprs_a_not_future(self, tramp: hp.Tramp) -> None:
            class Thing:
                def __repr__(s) -> str:
                    return "<REPR THING>"

            assert tramp.fut_to_string(Thing()) == "<REPR THING>"

        def test_says_if_the_future_is_pending(
            self, loop: asyncio.AbstractEventLoop, tramp: hp.Tramp
        ) -> None:
            fut: asyncio.Future[None] = loop.create_future()
            tramp.set_future_name(fut, name="one")
            assert tramp.fut_to_string(fut) == "<Future#one(pending)>"

            fut2: asyncio.Future[None] = loop.create_future()
            assert tramp.fut_to_string(fut2) == "<Future#None(pending)>"

        def test_says_if_the_future_is_cancelled(
            self, loop: asyncio.AbstractEventLoop, tramp: hp.Tramp
        ) -> None:
            fut: asyncio.Future[None] = loop.create_future()
            tramp.set_future_name(fut, name="one")
            fut.cancel()
            assert tramp.fut_to_string(fut) == "<Future#one(cancelled)>"

            fut2: asyncio.Future[None] = loop.create_future()
            fut2.cancel()
            assert tramp.fut_to_string(fut2) == "<Future#None(cancelled)>"

        def test_says_if_the_future_has_an_exception(
            self, loop: asyncio.AbstractEventLoop, tramp: hp.Tramp
        ) -> None:
            fut: asyncio.Future[None] = loop.create_future()
            tramp.set_future_name(fut, name="one")
            fut.set_exception(ValueError("HI"))
            assert tramp.fut_to_string(fut) == "<Future#one(exception:ValueError:HI)>"

            fut2: asyncio.Future[None] = loop.create_future()
            fut2.set_exception(TypeError("NOPE"))
            assert tramp.fut_to_string(fut2) == "<Future#None(exception:TypeError:NOPE)>"

        def test_says_if_the_future_has_a_result(
            self, loop: asyncio.AbstractEventLoop, tramp: hp.Tramp
        ) -> None:
            fut: asyncio.Future[bool] = loop.create_future()
            tramp.set_future_name(fut, name="one")
            fut.set_result(True)
            assert tramp.fut_to_string(fut) == "<Future#one(result)>"

            fut2: asyncio.Future[bool] = loop.create_future()
            fut2.set_result(False)
            assert tramp.fut_to_string(fut2) == "<Future#None(result)>"

    class TestLogException:
        def test_log_exception(
            self, log: logging.Logger, caplog: pytest.LogCaptureFixture
        ) -> None:
            tramp = hp.Tramp(log=log)

            error = ValueError("computer says no")
            exc_info: tuple[type[BaseException], BaseException, types.TracebackType]

            try:
                raise error
            except:
                _exc = sys.exc_info()
                assert _exc[0] is not None
                assert _exc[1] is not None
                assert _exc[2] is not None
                exc_info = _exc
            else:
                raise AssertionError("Exception should have been raised")

            tramp.log_exception(error, exc_info=exc_info)

            lines = [
                "ERROR    root:_context.py:* computer says no",
                "Traceback (most recent call last):",
                '  File "*test_context.py", line *, in test_log_exception',
                "    raise error",
                "ValueError: computer says no",
            ]

            matcher = pytest.LineMatcher(caplog.text.split("\n"))
            matcher.fnmatch_lines(lines)

    class TestSilentReporter:
        @pytest.fixture
        def tramp(self, log: logging.Logger) -> hp.Tramp:
            return hp.Tramp(log=log)

        async def test_does_nothing_if_the_future_was_cancelled(
            self,
            log: logging.Logger,
            caplog: pytest.LogCaptureFixture,
            loop: asyncio.AbstractEventLoop,
        ) -> None:
            tramp = hp.Tramp(log=log)
            fut: asyncio.Future[None] = loop.create_future()
            fut.cancel()

            tramp.silent_reporter(fut)
            assert caplog.text == ""

        async def test_does_nothing_if_the_future_has_an_exception(
            self,
            log: logging.Logger,
            caplog: pytest.LogCaptureFixture,
            loop: asyncio.AbstractEventLoop,
        ) -> None:
            tramp = hp.Tramp(log=log)
            fut: asyncio.Future[None] = loop.create_future()
            fut.set_exception(Exception("wat"))
            tramp.silent_reporter(fut)
            assert caplog.text == ""

        async def test_does_nothing_if_we_have_a_result(
            self,
            log: logging.Logger,
            caplog: pytest.LogCaptureFixture,
            loop: asyncio.AbstractEventLoop,
        ) -> None:
            @dataclasses.dataclass(frozen=True)
            class Res:
                name: str

            tramp = hp.Tramp(log=log)
            fut: asyncio.Future[Res] = loop.create_future()
            fut.set_result(Res(name="result"))
            tramp.silent_reporter(fut)
            assert caplog.text == ""

    class TestReporter:
        @pytest.fixture
        def tramp(self, log: logging.Logger) -> hp.Tramp:
            return hp.Tramp(log=log)

        async def test_does_nothing_if_the_future_was_cancelled(
            self,
            log: logging.Logger,
            caplog: pytest.LogCaptureFixture,
            loop: asyncio.AbstractEventLoop,
        ) -> None:
            tramp = hp.Tramp(log=log)
            fut: asyncio.Future[None] = loop.create_future()
            fut.cancel()
            tramp.reporter(fut)
            assert caplog.text == ""

        async def test_logs_exception_if_the_future_has_an_exception(
            self,
            log: logging.Logger,
            caplog: pytest.LogCaptureFixture,
            loop: asyncio.AbstractEventLoop,
        ) -> None:
            tramp = hp.Tramp(log=log)
            fut: asyncio.Future[None] = loop.create_future()

            try:
                raise Exception("computer says no")
            except Exception as e:
                fut.set_exception(e)

            tramp.reporter(fut)

            lines = [
                "ERROR    root:_context.py:* computer says no",
                "Traceback (most recent call last):",
                '  File "*test_context.py", line *, in test_logs_exception_if_the_future_has_an_exception',
                "    raise *",
                "Exception: computer says no",
            ]

            matcher = pytest.LineMatcher(caplog.text.split("\n"))
            matcher.fnmatch_lines(lines)

        async def test_it_does_nothing_if_we_have_a_result(
            self,
            log: logging.Logger,
            caplog: pytest.LogCaptureFixture,
            loop: asyncio.AbstractEventLoop,
        ) -> None:
            @dataclasses.dataclass(frozen=True)
            class Res:
                name: str

            tramp = hp.Tramp(log=log)
            fut: asyncio.Future[Res] = loop.create_future()
            fut.set_result(Res(name="result"))
            tramp.reporter(fut)
            assert caplog.text == ""


class TestCTX:
    async def test_has_helper_to_create_first_ctx(self, log: logging.Logger) -> None:
        tramp = hp.Tramp(log=log)
        loop = asyncio.get_event_loop_policy().get_event_loop()

        with hp.CTX.beginning(name="start", tramp=tramp) as ctx:
            assert ctx.loop is loop
            assert ctx.tramp is tramp
            assert ctx.name == "start"

            assert not ctx.done()
            assert not ctx.cancelled()
            with pytest.raises(asyncio.exceptions.InvalidStateError):
                ctx.exception()

            with ctx.child(name="child") as child:
                assert child.loop is loop
                assert child.tramp is tramp
                assert child.name == "start-->child"

                assert not child.done()
                assert not child.cancelled()
                with pytest.raises(asyncio.exceptions.InvalidStateError):
                    ctx.exception()

                child.cancel()

                assert child.done()
                assert child.cancelled()
                with pytest.raises(asyncio.CancelledError):
                    child.exception()

            assert not ctx.done()
            assert not ctx.cancelled()
            with pytest.raises(asyncio.exceptions.InvalidStateError):
                ctx.exception()

        assert ctx.done()
        assert ctx.cancelled()
        with pytest.raises(asyncio.CancelledError):
            ctx.exception()

    class TestAwaitingManagement:
        async def test_it_gets_earliest_exception(self, ctx: hp.CTX) -> None:
            class ComputerSaysNo(Exception):
                pass

            error1 = ComputerSaysNo("1")
            error2 = ComputerSaysNo("2")
            error3 = ComputerSaysNo("3")

            with ctx.child(name="one") as c1:
                with c1.child(name="two") as c2:
                    with c2.child(name="three") as c3:
                        with pytest.raises(asyncio.exceptions.InvalidStateError):
                            c1.exception()
                        with pytest.raises(asyncio.exceptions.InvalidStateError):
                            c2.exception()
                        with pytest.raises(asyncio.exceptions.InvalidStateError):
                            c3.exception()

                        c3.set_exception(error3)

                        with pytest.raises(asyncio.exceptions.InvalidStateError):
                            c1.exception()
                        with pytest.raises(asyncio.exceptions.InvalidStateError):
                            c2.exception()

                        assert c3.exception() is error3
                        assert not c3.cancelled()

                        with pytest.raises(ComputerSaysNo) as e:
                            await c3
                        assert str(e.value) == "3"

                    with pytest.raises(asyncio.exceptions.InvalidStateError):
                        c1.exception()
                    with pytest.raises(asyncio.exceptions.InvalidStateError):
                        c2.exception()

                    c2.set_exception(error2)
                    assert c2.exception() is error2
                    assert not c2.cancelled()
                    with pytest.raises(ComputerSaysNo) as e:
                        await c2
                    assert str(e.value) == "2"

                with pytest.raises(asyncio.exceptions.InvalidStateError):
                    c1.exception()

                c1.set_exception(error1)
                assert c1.exception() is error1
                assert not c1.cancelled()
                with pytest.raises(ComputerSaysNo) as e:
                    await c1
                assert str(e.value) == "1"

            assert c1.exception() is error1
            assert not c1.cancelled()
            with pytest.raises(ComputerSaysNo) as e:
                await c1
            assert str(e.value) == "1"

        async def test_it_gets_earliest_exception_even_if_parent_has_exception(
            self, ctx: hp.CTX
        ) -> None:
            class ComputerSaysNo(Exception):
                pass

            error2 = ComputerSaysNo("2")
            error3 = ComputerSaysNo("3")

            with ctx.child(name="one") as c1:
                with c1.child(name="two") as c2:
                    with c2.child(name="three") as c3:
                        with pytest.raises(asyncio.exceptions.InvalidStateError):
                            c1.exception()
                        with pytest.raises(asyncio.exceptions.InvalidStateError):
                            c2.exception()
                        with pytest.raises(asyncio.exceptions.InvalidStateError):
                            c3.exception()

                        c2.set_exception(error2)
                        c3.set_exception(error3)

                        with pytest.raises(asyncio.exceptions.InvalidStateError):
                            c1.exception()
                        assert not c1.cancelled()

                        assert c2.exception() is error2
                        assert not c2.cancelled()

                        assert c3.exception() is error3
                        assert not c3.cancelled()

                        with pytest.raises(ComputerSaysNo) as e:
                            await c3
                        assert str(e.value) == "3"

                        with pytest.raises(ComputerSaysNo) as e:
                            await c2
                        assert str(e.value) == "2"

        async def test_it_gets_earliest_exception_even_if_parent_is_cancelled(
            self, ctx: hp.CTX
        ) -> None:
            class ComputerSaysNo(Exception):
                pass

            error3 = ComputerSaysNo("3")

            with ctx.child(name="one") as c1:
                with c1.child(name="two") as c2:
                    with c2.child(name="three") as c3:
                        with pytest.raises(asyncio.exceptions.InvalidStateError):
                            c1.exception()
                        with pytest.raises(asyncio.exceptions.InvalidStateError):
                            c2.exception()
                        with pytest.raises(asyncio.exceptions.InvalidStateError):
                            c3.exception()

                        c1.cancel()
                        assert c1.cancelled()
                        assert c2.cancelled()
                        assert c3.cancelled()

                        with pytest.raises(asyncio.CancelledError):
                            c1.exception()
                        with pytest.raises(asyncio.CancelledError):
                            c2.exception()
                        with pytest.raises(asyncio.CancelledError):
                            c3.exception()

                        with pytest.raises(asyncio.CancelledError):
                            await c1
                        with pytest.raises(asyncio.CancelledError):
                            await c2

                        c3.set_exception(error3)
                        assert c1.cancelled()
                        assert c2.cancelled()
                        assert not c3.cancelled()

                        with pytest.raises(asyncio.CancelledError):
                            c1.exception()
                        with pytest.raises(asyncio.CancelledError):
                            c2.exception()

                        with pytest.raises(ComputerSaysNo) as e:
                            await c3
                        assert str(e.value) == "3"

        async def test_it_stops_waiting_on_first_parent_finishing(self, ctx: hp.CTX) -> None:
            waiter1: asyncio.Future[None] = ctx.loop.create_future()
            ctx.tramp.set_future_name(waiter1, name="waiter1")

            with ctx.child(name="one") as c1:
                with c1.child(name="two") as c2:
                    with c2.child(name="three") as c3:
                        e1 = asyncio.Event()

                        async def wait1() -> None:
                            e1.set()
                            with pytest.raises(asyncio.CancelledError):
                                await c3
                            waiter1.set_result(None)

                        task = ctx.async_as_background(wait1())
                        try:
                            await e1.wait()
                            assert not waiter1.done()

                            c1.cancel()
                            await waiter1
                        finally:
                            task.cancel()
                            await ctx.wait_for_all(task)

            class ComputerSaysNo(Exception):
                pass

            waiter2: asyncio.Future[None] = ctx.loop.create_future()
            ctx.tramp.set_future_name(waiter2, name="waiter2")
            with ctx.child(name="four") as c4:
                with c4.child(name="five") as c5:
                    with c5.child(name="six") as c6:
                        e2 = asyncio.Event()

                        async def wait2() -> None:
                            e2.set()
                            with pytest.raises(ComputerSaysNo):
                                await c6
                            waiter2.set_result(None)

                        task = ctx.async_as_background(wait2())
                        try:
                            await e2.wait()
                            assert not waiter2.done()

                            c5.set_exception(ComputerSaysNo())
                            await waiter2
                        finally:
                            task.cancel()
                            await ctx.wait_for_all(task)

            waiter3: asyncio.Future[None] = ctx.loop.create_future()
            ctx.tramp.set_future_name(waiter3, name="waiter3")
            with ctx.child(name="seven") as c7:
                with c7.child(name="eight") as c8:
                    with c8.child(name="nine") as c9:
                        event3 = asyncio.Event()

                        async def wait3() -> None:
                            event3.set()
                            with pytest.raises(asyncio.CancelledError):
                                await c9
                            waiter3.set_result(None)

                        task = ctx.async_as_background(wait3())
                        try:
                            await event3.wait()
                            assert not waiter3.done()

                            c9.cancel()
                            await waiter3
                        finally:
                            task.cancel()
                            await ctx.wait_for_all(task)

    class TestCallbackManagement:
        async def test_it_calls_callback_if_ctx_already_done(self, ctx: hp.CTX) -> None:
            called = CalledHelper()

            with ctx.child(name="1") as c1:
                c1.cancel()
                assert called == []
                e1 = asyncio.Event()
                c1.add_on_done(called.make_on_done(e1, c1, 1, asyncio.CancelledError))
                await e1.wait()
                assert called == [1]

                e2 = asyncio.Event()
                c1.add_done_callback(called.make_simpler_on_done(e2, 2, asyncio.CancelledError))
                await e2.wait()
                assert called == [1, 2]

            assert called == [1, 2]
            with pytest.raises(asyncio.CancelledError):
                await c1
            assert called == [1, 2]
            called.clear()

            with ctx.child(name="2") as c2, ctx.child(name="3") as c3:
                c2.cancel()
                assert c2.done()

                assert called == []

                failure = ValueError("Fail!")
                c3.set_exception(failure)
                with pytest.raises(ValueError):
                    await c3
                assert called == []

                e3 = asyncio.Event()
                c3.add_on_done(called.make_on_done(e3, c3, 3, failure))
                await e3.wait()
                assert called == [3]

                e4 = asyncio.Event()
                c3.add_done_callback(called.make_simpler_on_done(e4, 4, failure))
                await e4.wait()
                assert called == [3, 4]

            assert called == [3, 4]
            with pytest.raises(asyncio.CancelledError):
                await c2
            assert called == [3, 4]

            with pytest.raises(ValueError):
                await c3
            assert called == [3, 4]

        async def test_it_calls_callback_if_with_latest_exception(self, ctx: hp.CTX) -> None:
            called = CalledHelper()

            class ComputerSaysNo(Exception):
                pass

            error1 = ComputerSaysNo("1")
            error2 = ComputerSaysNo("2")
            error3 = ComputerSaysNo("3")

            with ctx.child(name="1") as c1:
                c1.set_exception(error1)

                assert called == []
                e1 = asyncio.Event()
                c1.add_on_done(called.make_on_done(e1, c1, 1, error1))
                await e1.wait()
                assert called == [1]

                e2 = asyncio.Event()
                c1.add_done_callback(called.make_simpler_on_done(e2, 2, error1))
                await e2.wait()
                assert called == [1, 2]

            assert called == [1, 2]
            with pytest.raises(ComputerSaysNo):
                await c1
            assert called == [1, 2]
            called.clear()

            with ctx.child(name="2") as c2:
                with c2.child(name="3") as c3:
                    c2.set_exception(error2)
                    c3.set_exception(error3)

                    assert called == []
                    e3 = asyncio.Event()
                    c3.add_on_done(called.make_on_done(e3, c3, 3, error3))
                    await e3.wait()
                    assert called == [3]

                    e4 = asyncio.Event()
                    c3.add_done_callback(called.make_simpler_on_done(e4, 4, error3))
                    await e4.wait()
                    assert called == [3, 4]

            assert called == [3, 4]
            with pytest.raises(ComputerSaysNo):
                await c2
            assert called == [3, 4]

            with pytest.raises(ComputerSaysNo):
                await c3
            assert called == [3, 4]

        async def test_it_calls_callback_on_first_failure(self, ctx: hp.CTX) -> None:
            called = CalledHelper()

            class ComputerSaysNo(Exception):
                pass

            error1 = ComputerSaysNo("1")

            with ctx.child(name="1") as c1:
                e1 = asyncio.Event()
                e2 = asyncio.Event()

                c1.add_on_done(called.make_on_done(e1, c1, "complex1", error1))
                c1.add_done_callback(called.make_simpler_on_done(e2, "simple1", error1))

                start = asyncio.Event()

                async def waiter1() -> None:
                    called.append(1)
                    start.set()
                    with pytest.raises(asyncio.CancelledError):
                        await c1

                task = ctx.async_as_background(waiter1())
                try:
                    assert called == []
                    await start.wait()
                    assert called == [1]

                    c1.set_exception(error1)
                    await e1.wait()
                    await e2.wait()
                    assert called == [1, "complex1", "simple1"]
                finally:
                    task.cancel()
                    await ctx.wait_for_all(task)

            assert called == [1, "complex1", "simple1"]
            with pytest.raises(ComputerSaysNo):
                await c1
            assert called == [1, "complex1", "simple1"]
            called.clear()

        async def test_it_calls_callback_on_first_failure_from_parent(self, ctx: hp.CTX) -> None:
            called = CalledHelper()

            class ComputerSaysNo(Exception):
                pass

            error1 = ComputerSaysNo("1")
            error2 = ComputerSaysNo("2")

            @contextlib.contextmanager
            def contexts() -> Iterator[tuple[hp.CTX, hp.CTX, hp.CTX, hp.CTX, hp.CTX]]:
                with ctx.child(name="1") as c1:
                    with c1.child(name="2") as c2:
                        with c2.child(name="3") as c3:
                            with c3.child(name="4") as c4:
                                with c4.child(name="5") as c5:
                                    yield c1, c2, c3, c4, c5

            with contexts() as (c1, c2, c3, c4, c5):
                e1 = asyncio.Event()
                e2 = asyncio.Event()
                c5.add_on_done(called.make_on_done(e1, c5, "complex1", error1))
                c5.add_done_callback(called.make_simpler_on_done(e2, "simple1", error1))

                e3 = asyncio.Event()
                e4 = asyncio.Event()
                c2.add_on_done(called.make_on_done(e3, c2, "complex2", error2))
                c2.add_done_callback(called.make_simpler_on_done(e4, "simple2", error2))

                start = asyncio.Event()

                async def waiter1() -> None:
                    called.append(1)
                    start.set()
                    with pytest.raises(asyncio.CancelledError):
                        await ctx

                task = ctx.async_as_background(waiter1())
                try:
                    assert called == []
                    await start.wait()
                    assert called == [1]

                    c3.set_exception(error1)
                    await e1.wait()
                    await e2.wait()
                    assert called == [1, "complex1", "simple1"]

                    with pytest.raises(ComputerSaysNo):
                        await c5
                    assert called == [1, "complex1", "simple1"]
                    called.clear()

                    assert not e3.is_set()
                    assert not e4.is_set()
                    c1.set_exception(error2)
                    await e3.wait()
                    await e4.wait()
                    assert called == ["complex2", "simple2"]

                    with pytest.raises(ComputerSaysNo) as e:
                        await c4
                    assert e.value == error1
                    assert called == ["complex2", "simple2"]

                    with pytest.raises(ComputerSaysNo) as e:
                        await c2
                    assert e.value == error2
                finally:
                    task.cancel()
                    await ctx.wait_for_all(task)

            assert called == ["complex2", "simple2"]
            called.clear()

            with pytest.raises(ComputerSaysNo):
                await c1
            assert called == []

        async def test_it_can_remove_callbacks(self, ctx: hp.CTX) -> None:
            called = CalledHelper()

            class ComputerSaysNo(Exception):
                pass

            error1 = ComputerSaysNo("1")
            error2 = ComputerSaysNo("2")

            @contextlib.contextmanager
            def contexts() -> Iterator[tuple[hp.CTX, hp.CTX, hp.CTX, hp.CTX, hp.CTX]]:
                with ctx.child(name="1") as c1:
                    with c1.child(name="2") as c2:
                        with c2.child(name="3") as c3:
                            with c3.child(name="4") as c4:
                                with c4.child(name="5") as c5:
                                    yield c1, c2, c3, c4, c5

            with contexts() as (c1, c2, c3, c4, c5):
                e1 = asyncio.Event()
                e2 = asyncio.Event()
                made1 = c5.add_on_done(called.make_on_done(e1, c5, "complex1", error1))
                made2 = c5.add_done_callback(called.make_simpler_on_done(e2, "simple1", error1))

                e3 = asyncio.Event()
                e4 = asyncio.Event()
                c2.add_on_done(called.make_on_done(e3, c2, "complex2", error2))
                c2.add_done_callback(called.make_simpler_on_done(e4, "simple2", error2))

                start = asyncio.Event()

                async def waiter1() -> None:
                    called.append(1)
                    start.set()
                    with pytest.raises(asyncio.CancelledError):
                        await ctx

                task = ctx.async_as_background(waiter1())
                try:
                    assert called == []
                    await start.wait()
                    assert called == [1]

                    c5.remove_done_callback(made1)
                    c5.remove_done_callback(made2)

                    c3.set_exception(error1)

                    with pytest.raises(ComputerSaysNo):
                        await c5
                    assert called == [1]
                    assert not e1.is_set()
                    assert not e2.is_set()

                    assert not e3.is_set()
                    assert not e4.is_set()
                    c1.set_exception(error2)
                    await e3.wait()
                    await e4.wait()
                    assert called == [1, "complex2", "simple2"]

                    with pytest.raises(ComputerSaysNo) as e:
                        await c4
                    assert e.value == error1
                    assert called == [1, "complex2", "simple2"]
                finally:
                    task.cancel()
                    await ctx.wait_for_all(task)

            assert called == [1, "complex2", "simple2"]
            called.clear()

            with pytest.raises(ComputerSaysNo):
                await c1
            assert called == []

        async def test_it_knows_if_context_has_direct_done_callback(self, ctx: hp.CTX) -> None:
            @contextlib.contextmanager
            def contexts() -> Iterator[tuple[hp.CTX, hp.CTX, hp.CTX]]:
                with ctx.child(name="1") as c1:
                    with c1.child(name="2") as c2:
                        with c2.child(name="3") as c3:
                            yield c1, c2, c3

            def on_done_1(res: hp.protocols.FutureStatus[None]) -> None:
                pass

            with contexts() as (c1, c2, c3):
                assert not c1.has_direct_done_callback(on_done_1)
                assert not c2.has_direct_done_callback(on_done_1)
                assert not c3.has_direct_done_callback(on_done_1)

                c2.add_done_callback(on_done_1)

                assert not c1.has_direct_done_callback(on_done_1)
                assert c2.has_direct_done_callback(on_done_1)
                assert not c3.has_direct_done_callback(on_done_1)

    class TestWaitForFirst:
        async def test_it_does_nothing_if_no_futures(self, ctx: hp.CTX) -> None:
            await ctx.wait_for_first()

        async def test_it_returns_if_any_futures_already_done(
            self, ctx: hp.CTX, loop: asyncio.AbstractEventLoop
        ) -> None:
            fut1: asyncio.Future[None] = loop.create_future()
            fut2: asyncio.Future[None] = loop.create_future()
            fut2.set_result(None)
            event1 = asyncio.Event()

            assert not fut1._callbacks
            assert not fut2._callbacks

            assert not fut1.done()
            assert fut2.done()

            await ctx.wait_for_first(fut1, fut2)
            assert not fut1.done()
            assert fut2.done()

            await ctx.wait_for_first(fut1, event1, fut2)
            assert not event1.is_set()
            assert not fut1.done()
            assert fut2.done()

            await ctx.wait_for_first(fut2, fut1)
            assert not fut1.done()
            assert fut2.done()

            await ctx.wait_for_first(fut2, fut1, fut1)
            assert not fut1.done()
            assert fut2.done()

            await ctx.wait_for_first(fut2, fut1, fut1, event1)
            assert not event1.is_set()
            assert not fut1.done()
            assert fut2.done()

            await ctx.wait_for_first(fut2, fut2, fut1)
            assert not fut1.done()
            assert fut2.done()

            assert not fut1._callbacks
            assert not fut2._callbacks

            event1.set()
            await ctx.wait_for_first(event1, fut1)
            assert event1.is_set()
            assert not fut1.done()

        async def test_it_can_wait_for_first_event(self, ctx: hp.CTX) -> None:
            called: list[object] = []
            async with hp.task_holder(ctx=ctx) as ts:
                fut1 = ctx.loop.create_future()
                fut2 = ctx.loop.create_future()
                event1 = asyncio.Event()

                ready = asyncio.Event()
                assert not any(event1._waiters)

                async def wait() -> None:
                    ready.set()
                    await ctx.wait_for_first(fut1, event1, fut2)
                    called.append("waited")

                waiting = ts.add_coroutine(wait())
                await ready.wait()
                assert called == []

                await asyncio.sleep(0.01)
                assert any(event1._waiters)
                event1.set()
                assert called == []

                await asyncio.sleep(0.01)
                assert waiting.done()
                assert not any(event1._waiters)
                assert called == ["waited"]

        async def test_it_returns_when_first_future_completes(
            self, ctx: hp.CTX, loop: asyncio.AbstractEventLoop, subtests: pytest_subtests.SubTests
        ) -> None:
            async def run_test(
                modify: Callable[[asyncio.Future[None]], None],
            ) -> asyncio.Future[None]:
                fut1: asyncio.Future[None] = loop.create_future()
                fut2: asyncio.Future[None] = loop.create_future()

                start = asyncio.Event()
                done = asyncio.Event()

                async def wait() -> None:
                    start.set()
                    await ctx.wait_for_first(fut1, fut2)
                    assert fut1.done()
                    assert not fut2.done()
                    assert not fut1._callbacks
                    assert not fut2._callbacks
                    done.set()

                assert not fut1._callbacks
                assert not fut2._callbacks

                ctx.async_as_background(wait())
                await start.wait()

                assert fut1._callbacks
                assert fut2._callbacks
                assert not fut1.done()
                assert not fut2.done()

                modify(fut1)

                await done.wait()

                assert fut1.done()
                assert not fut2.done()
                assert not fut1._callbacks
                assert not fut2._callbacks

                return fut1

            with subtests.test("normal_result"):

                def set_result(fut: asyncio.Future[None]) -> None:
                    fut.set_result(None)

                fut1 = await run_test(set_result)
                assert fut1.result() is None

            with subtests.test("set_exception"):

                class ComputerSaysNo(Exception):
                    pass

                error = ComputerSaysNo()

                def set_exception(fut: asyncio.Future[None]) -> None:
                    fut.set_exception(error)

                fut1 = await run_test(set_exception)
                assert fut1.exception() is error

            with subtests.test("cancel"):

                def cancel(fut: asyncio.Future[None]) -> None:
                    fut.cancel()

                fut1 = await run_test(cancel)
                assert fut1.cancelled()

    class TestWaitForAll:
        async def test_it_does_nothing_if_no_futures(self, ctx: hp.CTX) -> None:
            await ctx.wait_for_all()

        async def test_it_only_returns_if_all_futures_are_done(
            self, ctx: hp.CTX, loop: asyncio.AbstractEventLoop
        ) -> None:
            fut1: asyncio.Future[None] = loop.create_future()
            fut2: asyncio.Future[None] = loop.create_future()
            fut2.set_result(None)
            fut3: asyncio.Future[None] = loop.create_future()
            event = asyncio.Event()

            assert not fut1._callbacks
            assert not fut2._callbacks
            assert not fut3._callbacks
            assert not event._waiters

            assert not fut1.done()
            assert fut2.done()
            assert not fut3.done()
            assert not event.is_set()

            start = asyncio.Event()
            done = asyncio.Event()

            async def waiter() -> None:
                start.set()
                await ctx.wait_for_all(fut1, event, fut2, fut3, fut2)
                done.set()

            waiting = ctx.async_as_background(waiter())
            await start.wait()
            await asyncio.sleep(0.01)
            assert not done.is_set()

            assert fut1._callbacks
            assert not fut2._callbacks
            assert fut3._callbacks
            assert any(event._waiters)

            class ComputerSaysNo(Exception):
                pass

            error = ComputerSaysNo()

            fut1.set_exception(error)
            with pytest.raises(ComputerSaysNo):
                await fut1

            assert not done.is_set()
            assert not waiting.done()

            assert not fut1._callbacks
            assert not fut2._callbacks
            assert fut3._callbacks
            assert any(event._waiters)

            fut3.cancel()
            assert not done.is_set()
            assert not waiting.done()
            assert fut3.cancelled()

            assert not fut1._callbacks
            assert not fut2._callbacks
            assert not fut3._callbacks
            assert any(event._waiters)

            event.set()
            await done.wait()
            assert waiting.done()

            assert not fut1._callbacks
            assert not fut2._callbacks
            assert not fut3._callbacks
            assert not any(event._waiters)

            assert fut1.done()
            assert fut2.done()
            assert fut3.done()
            assert event.is_set()

    class TestAsyncWithTimeout:
        @pytest.fixture
        async def fake_mocked_later(self, ctx: hp.CTX) -> AsyncGenerator[thp.MockedCallLater]:
            async with thp.mocked_call_later(ctx=ctx) as m:
                yield m

        async def test_it_raises_cancelled_error_by_default_if_time_runs_out(
            self,
            fake_mocked_later: thp.MockedCallLater,
            ctx: hp.CTX,
            loop: asyncio.AbstractEventLoop,
        ) -> None:
            async def wait_forever() -> None:
                fut: asyncio.Future[None] = loop.create_future()
                try:
                    await fut
                finally:
                    fut.cancel()

            now = time.time()
            with pytest.raises(asyncio.CancelledError):
                await ctx.async_with_timeout(wait_forever(), timeout=10, name="wait_forever")

            assert 9 < time.time() - now < 11

        async def test_it_uses_alternate_error_if_provided(
            self,
            fake_mocked_later: thp.MockedCallLater,
            ctx: hp.CTX,
            loop: asyncio.AbstractEventLoop,
        ) -> None:
            class ComputerSaysNo(Exception):
                pass

            async def wait_forever() -> None:
                fut: asyncio.Future[None] = loop.create_future()
                try:
                    await fut
                finally:
                    fut.cancel()

            now = time.time()
            error = ComputerSaysNo()

            with pytest.raises(ComputerSaysNo) as e:
                await ctx.async_with_timeout(
                    wait_forever(), timeout=10, timeout_error=error, name="wait_forever"
                )

            assert 9 < time.time() - now < 11
            assert e.value is error

        async def test_it_passes_on_result(
            self,
            fake_mocked_later: thp.MockedCallLater,
            ctx: hp.CTX,
            loop: asyncio.AbstractEventLoop,
        ) -> None:
            async def wait_forever() -> int:
                fut: asyncio.Future[int] = loop.create_future()
                loop.call_later(1, fut.set_result, 40)
                return await fut

            now = time.time()
            assert (
                await ctx.async_with_timeout(wait_forever(), timeout=10, name="get_result")
            ) == 40
            assert 0 < time.time() - now < 2

        async def test_it_passes_on_exception(
            self,
            fake_mocked_later: thp.MockedCallLater,
            ctx: hp.CTX,
            loop: asyncio.AbstractEventLoop,
        ) -> None:
            class ComputerSaysNo(Exception):
                pass

            error = ComputerSaysNo()

            async def wait_forever() -> int:
                fut: asyncio.Future[int] = loop.create_future()
                loop.call_later(3, fut.set_exception, error)
                return await fut

            now = time.time()
            with pytest.raises(ComputerSaysNo) as e:
                await ctx.async_with_timeout(wait_forever(), timeout=10, name="get_exception")

            assert 2 < time.time() - now < 4
            assert e.value is error

        async def test_it_passes_on_cancellation(
            self,
            fake_mocked_later: thp.MockedCallLater,
            ctx: hp.CTX,
            loop: asyncio.AbstractEventLoop,
        ) -> None:
            async def wait_forever() -> int:
                fut: asyncio.Future[int] = loop.create_future()
                loop.call_later(2, fut.cancel)
                return await fut

            now = time.time()
            with pytest.raises(asyncio.CancelledError):
                await ctx.async_with_timeout(wait_forever(), timeout=10, name="get_cancelled")

            assert 1 < time.time() - now < 3

        async def test_it_passes_on_even_if_custom_timeout_error(
            self,
            fake_mocked_later: thp.MockedCallLater,
            ctx: hp.CTX,
            loop: asyncio.AbstractEventLoop,
        ) -> None:
            class ComputerSaysNo(Exception):
                pass

            async def wait_forever() -> int:
                fut: asyncio.Future[int] = loop.create_future()
                loop.call_later(2, fut.cancel)
                return await fut

            now = time.time()
            error = ComputerSaysNo()
            with pytest.raises(asyncio.CancelledError):
                await ctx.async_with_timeout(
                    wait_forever(), timeout=10, timeout_error=error, name="get_cancelled"
                )

            assert 1 < time.time() - now < 3

        async def test_it_can_signal_when_timeout_happens_before_task_is_cleaned_up(
            self, fake_mocked_later: thp.MockedCallLater, ctx: hp.CTX
        ) -> None:
            got: list[object] = []
            done = asyncio.Event()

            async def wait_forever() -> None:
                event = asyncio.Event()
                try:
                    got.append((time.time(), "waiting"))
                    await event.wait()
                except asyncio.CancelledError:
                    got.append((time.time(), "cancelled"))
                    event2 = asyncio.Event()
                    ctx.loop.call_later(2, event2.set)
                    await event2.wait()
                    got.append((time.time(), "done"))
                    done.set()

            timeout_event = asyncio.Event()

            async with hp.task_holder(ctx=ctx) as ts:

                async def wait_for_timeout() -> None:
                    await timeout_event.wait()
                    got.append((time.time(), "timeout_happened"))

                ts.add_coroutine(wait_for_timeout())

                with pytest.raises(asyncio.CancelledError):
                    await ctx.async_with_timeout(
                        wait_forever(),
                        timeout=10,
                        name="get_cancelled",
                        timeout_event=timeout_event,
                    )

            got.append((time.time(), "finished"))
            await done.wait()

            assert got == [
                (
                    0,
                    "waiting",
                ),
                (
                    10,
                    "timeout_happened",
                ),
                (
                    10,
                    "cancelled",
                ),
                (
                    12,
                    "done",
                ),
                (
                    12,
                    "finished",
                ),
            ]

        async def test_it_allows_task_to_cleanup(
            self, fake_mocked_later: thp.MockedCallLater, ctx: hp.CTX
        ) -> None:
            got: list[object] = []
            done = asyncio.Event()

            class ComputerSaysNo(Exception):
                pass

            error = ComputerSaysNo()

            async def wait_forever() -> None:
                event = asyncio.Event()
                try:
                    got.append((time.time(), "waiting"))
                    await event.wait()
                except asyncio.CancelledError:
                    got.append((time.time(), "cancelled"))
                    event2 = asyncio.Event()
                    ctx.loop.call_later(2, event2.set)
                    await event2.wait()
                    got.append((time.time(), "done"))
                    done.set()

            timeout_event = asyncio.Event()

            async with hp.task_holder(ctx=ctx) as ts:

                async def wait_for_timeout() -> None:
                    await timeout_event.wait()
                    got.append((time.time(), "timeout_happened"))

                ts.add_coroutine(wait_for_timeout())

                with pytest.raises(ComputerSaysNo) as e:
                    await ctx.async_with_timeout(
                        wait_forever(),
                        timeout=10,
                        name="get_cancelled",
                        timeout_event=timeout_event,
                        timeout_error=error,
                    )

            assert e.value == error

            got.append((time.time(), "finished"))
            await done.wait()

            assert got == [
                (
                    0,
                    "waiting",
                ),
                (
                    10,
                    "timeout_happened",
                ),
                (
                    10,
                    "cancelled",
                ),
                (
                    12,
                    "done",
                ),
                (
                    12,
                    "finished",
                ),
            ]

        async def test_it_does_not_set_timeout_event_if_coroutine_returns_before_timeout(
            self, fake_mocked_later: thp.MockedCallLater, ctx: hp.CTX
        ) -> None:
            async def wait_a_couple_seconds() -> int:
                fut: asyncio.Future[int] = ctx.loop.create_future()
                ctx.loop.call_later(2, fut.set_result, 3)
                return await fut

            timeout_event = asyncio.Event()

            assert 3 == await ctx.async_with_timeout(
                wait_a_couple_seconds(),
                timeout=10,
                name="get_cancelled",
                timeout_event=timeout_event,
            )

            assert not timeout_event.is_set()
            assert time.time() == 2
            await asyncio.sleep(11)
            assert time.time() == 13
            assert not timeout_event.is_set()

        async def test_it_does_not_set_timeout_event_if_coroutine_raises_exception_before_timeout(
            self, fake_mocked_later: thp.MockedCallLater, ctx: hp.CTX
        ) -> None:
            class ComputerSaysNo(Exception):
                pass

            error = ComputerSaysNo()

            async def wait_a_couple_seconds() -> int:
                fut: asyncio.Future[int] = ctx.loop.create_future()
                ctx.loop.call_later(2, fut.set_exception, error)
                return await fut

            timeout_event = asyncio.Event()

            with pytest.raises(ComputerSaysNo) as e:
                await ctx.async_with_timeout(
                    wait_a_couple_seconds(),
                    timeout=10,
                    name="get_cancelled",
                    timeout_event=timeout_event,
                )

            assert e.value == error

            assert not timeout_event.is_set()
            assert time.time() == 2
            await asyncio.sleep(11)
            assert time.time() == 13
            assert not timeout_event.is_set()

        async def test_it_does_not_set_timeout_event_if_coroutine_cancels_itself_before_timeout(
            self, fake_mocked_later: thp.MockedCallLater, ctx: hp.CTX
        ) -> None:
            async def wait_a_couple_seconds() -> int:
                fut: asyncio.Future[int] = ctx.loop.create_future()
                ctx.loop.call_later(2, fut.cancel)
                return await fut

            timeout_event = asyncio.Event()

            with pytest.raises(asyncio.CancelledError):
                await ctx.async_with_timeout(
                    wait_a_couple_seconds(),
                    timeout=10,
                    name="get_cancelled",
                    timeout_event=timeout_event,
                )

            assert not timeout_event.is_set()
            assert time.time() == 2
            await asyncio.sleep(11)
            assert time.time() == 13
            assert not timeout_event.is_set()
