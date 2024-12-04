from typing import Dict

from pydantic import BaseModel

from app.domain.enum.enum import ModelName


class LlmData(BaseModel):
    model: ModelName
    path: str
    prompt: Dict[str, str]


class Result(BaseModel):
    reception_id: str


class ReceptionRequest(BaseModel):
    session_id: int
    polling: bool
    body: LlmData


class ReceptionResponse(BaseModel):
    session_id: int
    result: Result
