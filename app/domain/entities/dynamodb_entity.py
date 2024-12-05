from datetime import datetime
from typing import Dict

from pydantic import BaseModel

from app.domain.enum.enum import (
    DynamoDBStatus,
    SystemName,
)
from app.domain.enum.llm_enum import AnthropicModelName, GoogleModelName


class DynamoDBData(BaseModel):
    id: str
    group_id: str
    group_index: int
    system: SystemName
    status: DynamoDBStatus
    model: AnthropicModelName | GoogleModelName
    path: str
    input: Dict[str, str]
    result: Dict[str, str] = {}
    create_at: datetime = datetime.now()
    update_at: datetime = datetime.now()
