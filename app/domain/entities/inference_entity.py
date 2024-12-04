from pydantic import BaseModel


class SQSData(BaseModel):
    reception_id: str
    polling: bool


class InferenceRequest(BaseModel):
    session_id: int
    message_id: str
    body: SQSData


class InferenceResponse(BaseModel):
    message_id: str
    result: str
