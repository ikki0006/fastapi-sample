from typing import Dict, List

from pydantic import BaseModel

from app.domain.enum.enum import SystemName
from app.domain.enum.llm_enum import AnthropicModelName, GoogleModelName


class LlmData(BaseModel):
    model: AnthropicModelName | GoogleModelName
    path: str
    prompt: Dict[str, str]


class Result(BaseModel):
    reception_ids: List[str]
    group_id: str


class ReceptionRequest(BaseModel):
    session_id: int
    polling: bool
    system: SystemName
    body: List[LlmData]


class ReceptionResponse(BaseModel):
    session_id: int
    result: Result
