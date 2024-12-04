from ulid import ULID

from app.domain.entities.dynamodb_entity import DynamoDBData
from app.domain.entities.reception_entity import (
    ReceptionRequest,
    ReceptionResponse,
    Result,
)
from app.domain.enum.enum import DynamoDBStatus
from app.infrastructure.aws.dynamodb import DynamoDB_Client


class ReceptionUsecase:
    def __init__(
        self, receptionRequest: ReceptionRequest, dynamoDB_client: DynamoDB_Client
    ) -> None:
        self.dynamoDB_client = dynamoDB_client
        self.request = receptionRequest

    def handle_queue_reception(self) -> ReceptionResponse:
        session_id: int = self.request.session_id
        reception_id: str = str(ULID())
        table = self.dynamoDB_client.get_table_name(self.request.polling)
        data: DynamoDBData = DynamoDBData(
            id=reception_id,
            status=DynamoDBStatus.Queued,
            model=self.request.body.model,
            path=self.request.body.path,
            input=self.request.body.prompt,
            result={},
        )
        self.dynamoDB_client.put_item(table, data)
        return ReceptionResponse(
            session_id=session_id, result=Result(**{"reception_id": reception_id})
        )
