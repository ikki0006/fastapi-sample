from typing import List

from pydantic import BaseModel

from app.domain.entities.dynamodb_entity import DynamoDBData


class SQSData(BaseModel):
    reception_ids: List[str]
    polling: bool


class InferenceRequest(BaseModel):
    session_id: int
    message_id: str
    body: SQSData


class InferenceResponse(BaseModel):
    message_id: str
    result: str


class GetInferenceResponse(BaseModel):
    result: DynamoDBData
