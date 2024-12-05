from typing import Optional

from pydantic import BaseModel

from app.domain.enum.llm_enum import LLMRole


class LLMApiResponse(BaseModel):
    id: str
    model: str
    content: str
    role: LLMRole
    input_tokens: Optional[int]
    output_tokens: Optional[int]
