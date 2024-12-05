from fastapi import APIRouter

from app.domain.entities.inference_entity import InferenceRequest, InferenceResponse
from app.domain.usecases.inference_usecase import InferenceUsecase
from app.infrastructure.aws.dynamodb import DynamoDB_Client
from app.infrastructure.llm.anthoropic import AnthoropicApi

router = APIRouter(tags=["inference"])


@router.post("/inference")
def read_root(inferenceRequest: InferenceRequest) -> InferenceResponse:
    dynamoDB_client = DynamoDB_Client()
    anthoropicApi = AnthoropicApi()
    inferenceUsecase = InferenceUsecase(
        inferenceRequest, dynamoDB_client, anthoropicApi
    )
    response: InferenceResponse = inferenceUsecase.handle_llm_inference()

    return response
