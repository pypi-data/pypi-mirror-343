from enum import Enum


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    SCHEMA = "schema"


class Provider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


class Author(Enum):
    HUMAN = "human"
    MACHINE = "machine"
