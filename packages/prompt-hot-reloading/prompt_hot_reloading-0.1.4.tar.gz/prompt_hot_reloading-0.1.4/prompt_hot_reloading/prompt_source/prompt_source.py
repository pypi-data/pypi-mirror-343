from abc import ABC, abstractmethod
from typing import Callable


class PromptSource(ABC):
    @abstractmethod
    def load_all(self) -> dict[str, str]:
        """Return a map name→text of every prompt currently available."""
        pass

    @abstractmethod
    def watch(self, on_change: Callable[[str, str], None]) -> None:
        """
        Start background watching. Whenever a prompt is created/updated,
        call on_change(name, new_text). Should run in a daemon thread.
        """
        pass
