from app.domain.entities.inference_entity import (
    InferenceRequest,
    InferenceResponse,
)
from app.infrastructure.aws.dynamodb import DynamoDB_Client


class InferenceUsecase:
    def __init__(
        self, inferenceRequest: InferenceRequest, dynamoDB_client: DynamoDB_Client
    ) -> None:
        self.dynamoDB_client = dynamoDB_client
        self.request = inferenceRequest

    def handle_llm_inference(self) -> InferenceResponse:
        # session_id: int = self.request.session_id
        reception_id: str = self.request.body.reception_id
        table = self.dynamoDB_client.get_table_name(self.request.body.polling)
        self.dynamoDB_client.get_item(table, reception_id)
        return InferenceResponse(message_id=self.request.message_id, result="success")
