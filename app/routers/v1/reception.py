from fastapi import APIRouter

from app.domain.entities.reception_entity import ReceptionRequest, ReceptionResponse
from app.domain.usecases.reception_usecase import ReceptionUsecase
from app.infrastructure.aws.dynamodb import DynamoDB_Client

router = APIRouter(tags=["reception"])


@router.post("/reception")
def post_reception(receptionRequest: ReceptionRequest) -> ReceptionResponse:
    dynamoDB_client = DynamoDB_Client()
    receptionUsecase = ReceptionUsecase(receptionRequest, dynamoDB_client)
    response: ReceptionResponse = receptionUsecase.handle_queue_reception()

    return response
