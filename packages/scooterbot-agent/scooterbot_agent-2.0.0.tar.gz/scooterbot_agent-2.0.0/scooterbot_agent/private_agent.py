from abc import ABC

from .agent import ScooterbotAgent


class PrivateAgent(ScooterbotAgent, ABC):
    user_id: str

    def __init__(self, user_id: str):
        self.user_id = user_id
