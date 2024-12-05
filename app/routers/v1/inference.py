from fastapi import APIRouter

from app.domain.entities.inference_entity import (
    GetInferenceResponse,
    InferenceRequest,
    InferenceResponse,
)
from app.domain.usecases.inference_usecase import GetInferenceUsecase, InferenceUsecase
from app.infrastructure.aws.dynamodb import DynamoDB_Client
from app.infrastructure.llm.anthoropic import AnthoropicApi

router = APIRouter(tags=["inference"])


@router.post("/inference")
def post_inference(inferenceRequest: InferenceRequest) -> InferenceResponse:
    dynamoDB_client = DynamoDB_Client()
    anthoropicApi = AnthoropicApi()
    inference_usecase = InferenceUsecase(
        inferenceRequest, dynamoDB_client, anthoropicApi
    )
    response: InferenceResponse = inference_usecase.handle_llm_inference()

    return response


@router.get("/inference/{id}")
def get_inference(id: str, polling: bool) -> GetInferenceResponse:
    dynamoDB_client = DynamoDB_Client()
    get_inference_usecase = GetInferenceUsecase(dynamoDB_client, polling)
    response: GetInferenceResponse = get_inference_usecase.get_inference(id=id)

    return response
