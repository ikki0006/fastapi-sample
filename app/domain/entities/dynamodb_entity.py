from typing import Dict

from pydantic import BaseModel

from app.domain.enum.enum import DynamoDBStatus, ModelName


class DynamoDBData(BaseModel):
    id: str
    status: DynamoDBStatus
    model: ModelName
    path: str
    input: Dict[str, str]
    result: Dict[str, str]
