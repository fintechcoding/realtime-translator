import asyncio
from collections import defaultdict
from typing import Any, Callable, Coroutine

from app.utils.logger import log


class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)

    def on(self, event: str, handler: Callable[..., Coroutine | None]):
        self._handlers[event].append(handler)

    def off(self, event: str, handler: Callable):
        if event in self._handlers:
            self._handlers[event] = [h for h in self._handlers[event] if h != handler]

    async def emit(self, event: str, *args: Any, **kwargs: Any):
        for handler in self._handlers.get(event, []):
            try:
                result = handler(*args, **kwargs)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                log.error(f"EventBus handler error on '{event}': {e}")

    def emit_sync(self, event: str, *args: Any, **kwargs: Any):
        loop = None
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            pass

        if loop and loop.is_running():
            asyncio.ensure_future(self.emit(event, *args, **kwargs))
        else:
            for handler in self._handlers.get(event, []):
                try:
                    result = handler(*args, **kwargs)
                    if asyncio.iscoroutine(result):
                        log.warning(f"Async handler for '{event}' called from sync context, skipping")
                except Exception as e:
                    log.error(f"EventBus sync handler error on '{event}': {e}")
