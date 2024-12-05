from enum import Enum


class AnthropicModelName(Enum):
    CLAUDE_3_5_SONET_20241022 = "claude-3-5-sonnet-20241022"
    CLAUDE_3_5_HAIKU_20241022 = "claude-3-5-haiku-20241022"


class GoogleModelName(Enum):
    Gemimi = "gemimi"


class DynamoDBStatus(Enum):
    ERROR = "error"
    SUCCESS = "success"
    Queued = "queued"


class SystemName(Enum):
    RESUME_MATCH = "resume_match"
    JOB_POSTING = "job_posting"
    DIRECT_SCOUT = "direct_scout"
