from enum import Enum


class AnthropicModelName(Enum):
    CLAUDE_3_5_SONET_20241022 = "claude-3-5-sonnet-20241022"
    CLAUDE_3_5_HAIKU_20241022 = "claude-3-5-haiku-20241022"


class GoogleModelName(Enum):
    Gemimi = "gemimi"


class LLMRole(Enum):
    ASSISTANT = "assistant"
    USER = "user"
    SYSTEM = "system"
