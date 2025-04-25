from abc import ABC
from abc import abstractmethod


class ScooterbotAgent(ABC):
    @abstractmethod
    def reply(self, message: str) -> str:
        """Reply to a message from the user."""
