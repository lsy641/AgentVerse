from typing import List

from pydantic import Field

from agentverse.message import Message

from . import memory_registry
from .base import BaseMemory


@memory_registry.register("chat_history")
class ChatHistoryMemory(BaseMemory):
    messages: List[Message] = Field(default=[])

    def add_message(self, messages: List[Message]) -> None:
        for message in messages:
            self.messages.append(message)

    def to_string(
        self,
        add_sender_prefix: bool = False,
        start_index: int = 0,
        end_index: int = None,
    ) -> str:
        if add_sender_prefix:
            return "\n".join(
                [
                    f"[{message.sender}]: {message.content}"
                    if message.sender != ""
                    else message.content
                    for message in self.messages[start_index:end_index]
                ]
            )
        else:
            return "\n".join(
                [message.content for message in self.messages[start_index:end_index]]
            )

    def reset(self) -> None:
        self.messages = []
