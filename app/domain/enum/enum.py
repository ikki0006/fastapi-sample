from enum import Enum


class DynamoDBStatus(Enum):
    ERROR = "error"
    SUCCESS = "success"
    Queued = "queued"


class SystemName(Enum):
    RESUME_MATCH = "resume_match"
    JOB_POSTING = "job_posting"
    DIRECT_SCOUT = "direct_scout"
