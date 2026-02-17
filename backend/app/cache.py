from __future__ import annotations

import time
from threading import Lock
from typing import Any, Optional


class TTLCache:
    def __init__(self, default_ttl_seconds: int = 60) -> None:
        self._default_ttl = int(default_ttl_seconds)
        self._store: dict[str, tuple[float, Any]] = {}
        self._lock = Lock()

    def get(self, key: str) -> Optional[Any]:
        now = time.time()

        with self._lock:
            item = self._store.get(key)
            if item is None:
                return None

            expires_at, value = item
            if now >= expires_at:
                self._store.pop(key, None)
                return None

            return value

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        ttl = self._default_ttl if ttl_seconds is None else int(ttl_seconds)
        expires_at = time.time() + ttl

        with self._lock:
            self._store[key] = (expires_at, value)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()
