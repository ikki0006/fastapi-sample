from ulid import ULID

from app.domain.entities.reception_entity import (
    ReceptionRequest,
    ReceptionResponse,
    Result,
)
from app.infrastructure.aws.dynamodb import DynamoDB_Client


class ReceptionUsecase:
    def __init__(
        self, receptionRequest: ReceptionRequest, dynamoDB_client: DynamoDB_Client
    ) -> None:
        self.dynamoDB_client = dynamoDB_client
        self.request = receptionRequest

    def handle_queue_reception(self) -> ReceptionResponse:
        session_id: int = self.request.session_id
        id: str = str(ULID())
        table = self.dynamoDB_client.get_table_name(self.request.polling)
        item = {"id": {"S": id}, "session_id": {"N": str(session_id)}}
        self.dynamoDB_client.put_item(table, item)
        return ReceptionResponse(session_id=session_id, result=Result(**{"id": id}))
