from typing import List

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
        group_id: str = str(ULID())
        self.dynamoDB_client.get_table_name(self.request.polling)
        data_list: List[DynamoDBData] = []
        id_list: List[str] = []
        for index, data in enumerate(self.request.body):
            id: str = str(ULID())
            dynamodb_data: DynamoDBData = DynamoDBData(
                id=id,
                group_id=group_id,
                group_index=index,
                status=DynamoDBStatus.Queued,
                system=self.request.system,
                model=data.model,
                path=data.path,
                input=data.prompt,
            )
            id_list.append(id)
            data_list.append(dynamodb_data)

        self.dynamoDB_client.batch_put_item(data_list)
        return ReceptionResponse(
            session_id=session_id,
            result=Result(reception_ids=id_list, group_id=group_id),
        )
