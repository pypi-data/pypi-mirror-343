import asyncio
import signal
import traceback
import types


class AsyncBlock:
    def __init__(self, timeout: int = 30):
        self._timeout = timeout
        self._orig_run = None

    def start(self) -> None:
        def _run(handle: asyncio.Handle):
            signal.alarm(self._timeout)
            try:
                self._orig_run(handle)
            finally:
                signal.alarm(0)

        self._orig_run = asyncio.events.Handle._run

        signal.signal(signal.SIGALRM, self._message)

        asyncio.events.Handle._run = _run

    def shutdown(self) -> None:
        asyncio.events.Handle._run = self._orig_run
        signal.signal(signal.SIGALRM, signal.SIG_IGN)

    def _message(self, _: int, frame: types.FrameType | None) -> None:
        stack = [stack for stack in reversed(traceback.extract_stack(frame))][0]
        func, file, lineno, code = stack.name, stack.filename, stack.lineno, stack.line.strip() if stack.line else ""
        logger.warning(
            f"Event loop is blocked for {self._timeout} sec in location {file}:{lineno} in {func}() → {code}"
        )


__all__ = ["AsyncBlock"]
