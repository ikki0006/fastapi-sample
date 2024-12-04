from typing import Dict

from pydantic import BaseModel


class LlmData(BaseModel):
    model: str
    path: str
    prompt: Dict[str, str]


class Result(BaseModel):
    id: str


class ReceptionRequest(BaseModel):
    session_id: int
    polling: bool
    data: LlmData


class ReceptionResponse(BaseModel):
    session_id: int
    result: Result
