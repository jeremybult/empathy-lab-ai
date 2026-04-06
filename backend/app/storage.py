from threading import Lock
from typing import Dict, List


class MemoryConversationStore:
    def __init__(self, max_messages: int = 12) -> None:
        self.max_messages = max_messages
        self._data: Dict[str, List[dict]] = {}
        self._lock = Lock()

    def get_history(self, key: str) -> List[dict]:
        with self._lock:
            return list(self._data.get(key, []))

    def append(self, key: str, message: dict) -> List[dict]:
        with self._lock:
            history = self._data.setdefault(key, [])
            history.append(message)
            if len(history) > self.max_messages:
                del history[:-self.max_messages]
            return list(history)

    def replace(self, key: str, history: List[dict]) -> None:
        with self._lock:
            self._data[key] = list(history[-self.max_messages:])

    def reset(self, key: str) -> None:
        with self._lock:
            self._data[key] = []
