from fastapi import APIRouter

from app.domain.entities.inference_entity import InferenceRequest, InferenceResponse
from app.domain.usecases.inference_usecase import InferenceUsecase
from app.infrastructure.aws.dynamodb import DynamoDB_Client

router = APIRouter(tags=["inference"])


@router.post("/inference")
def read_root(inferenceRequest: InferenceRequest) -> InferenceResponse:
    dynamoDB_client = DynamoDB_Client()
    inferenceUsecase = InferenceUsecase(inferenceRequest, dynamoDB_client)
    response: InferenceResponse = inferenceUsecase.handle_llm_inference()

    return response
