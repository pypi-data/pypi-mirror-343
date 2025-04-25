from functools import partial
from threading import Thread
from typing import Callable

from lcm import LCM

from lcmutils.typing import LCMHandler


class LCMDaemon:
    """
    Daemon that handles LCM messages in a separate thread.
    """

    def __init__(
        self,
        lcm: LCM | None = None,
        start: bool = False,
        timeout_millis: int | None = None,
    ) -> None:
        self._lcm = lcm or LCM()
        self._timeout_millis = timeout_millis
        self._thread = Thread(target=self._run, daemon=True)
        self._running = False
        if start:
            self.start()

    @property
    def lcm(self) -> LCM:
        """
        Get the LCM instance.

        Returns:
            LCM: LCM instance.
        """
        return self._lcm

    def _run(self) -> None:
        """
        Handle LCM messages until the daemon is stopped.
        """
        handle_function = (
            partial(self._lcm.handle_timeout, self._timeout_millis)
            if self._timeout_millis is not None
            else self._lcm.handle
        )

        while self._running:
            handle_function()

    def start(self) -> None:
        """
        Start the daemon.
        """
        self._running = True
        self._thread.start()

    def stop(self) -> None:
        """
        Stop the daemon.
        """
        self._running = False
        self._thread.join()

    def subscribe(self, *channel: tuple[str]) -> Callable[[LCMHandler], LCMHandler]:
        """
        Create a decorator to subscribe a function to one or more channels.

        Args:
            channel (tuple[str]): Channel(s) to subscribe to.

        Returns:
            callable: Decorator that subscribes a function to the channel.
        """

        def decorator(handler: LCMHandler) -> LCMHandler:
            for c in channel:
                self._lcm.subscribe(c, handler)
            return handler

        return decorator


__all__ = ["LCMDaemon"]
