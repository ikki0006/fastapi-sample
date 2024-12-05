import logging
from datetime import datetime
from typing import Dict

from jinja2 import Template

from app.core.utils.file import file_loader
from app.domain.entities.dynamodb_entity import DynamoDBData
from app.domain.entities.inference_entity import (
    GetInferenceResponse,
    InferenceRequest,
    InferenceResponse,
)
from app.domain.entities.llm_entity import LLMApiResponse
from app.domain.enum.enum import DynamoDBStatus
from app.domain.enum.llm_enum import AnthropicModelName, GoogleModelName
from app.infrastructure.aws.dynamodb import DynamoDB_Client
from app.infrastructure.llm.anthoropic import AnthoropicApi

_logger = logging.getLogger(f"custom.{__name__}")


class InferenceUsecase:
    def __init__(
        self,
        inferenceRequest: InferenceRequest,
        dynamoDB_client: DynamoDB_Client,
        anthoropicApi: AnthoropicApi,
    ) -> None:
        self.dynamoDB_client = dynamoDB_client
        self.request = inferenceRequest
        self.anthoropicApi = anthoropicApi

    def handle_llm_inference(self) -> InferenceResponse:
        # session_id: int = self.request.session_id

        self.dynamoDB_client.get_table_name(self.request.body.polling)
        last_responses: str = ""
        for id in self.request.body.reception_ids:
            dynamodb_data: DynamoDBData = self.dynamoDB_client.get_item(key=id)
            if last_responses != "":
                dynamodb_data.input["last_responses"] = last_responses
            result = self._llm_inference(dynamodb_data)
            if result is None:
                return InferenceResponse(
                    message_id=self.request.message_id, result="error"
                )
            last_responses = result
        return InferenceResponse(message_id=self.request.message_id, result="success")

    def _llm_inference(self, dynamodb_data: DynamoDBData) -> str | None:
        try:
            prompt = self.create_prompt(dynamodb_data.path, dynamodb_data.input)
            response = self.choice_llm(dynamodb_data, prompt)
            dynamodb_data.update_at = datetime.now()
            if response is not None:
                dynamodb_data.result = {"result": response.content}
                dynamodb_data.status = DynamoDBStatus.SUCCESS
                self.dynamoDB_client.put_item(dynamodb_data)
                return response.content
            return None

        except Exception as e:
            _logger.error("error:", e)
            dynamodb_data.status = DynamoDBStatus.ERROR
            dynamodb_data.update_at = datetime.now()
            self.dynamoDB_client.put_item(dynamodb_data)
            return None

    # テンプレートエンジンを使って、promptを生成
    def create_prompt(
        self,
        path: str,
        input: Dict[str, str],
    ) -> str:
        template = Template(file_loader(path))
        prompt: str = template.render(input)
        return prompt

    def choice_llm(
        self, dynamodb_data: DynamoDBData, prompt: str
    ) -> LLMApiResponse | None:
        if type(dynamodb_data.model) is AnthropicModelName:
            return self.anthoropicApi.generate(
                model_name=dynamodb_data.model,
                message=prompt,
            )
        elif type(dynamodb_data.model) is GoogleModelName:
            pass

        return None


class GetInferenceUsecase:
    def __init__(
        self,
        dynamoDB_client: DynamoDB_Client,
        polling: bool,
    ) -> None:
        self.dynamoDB_client = dynamoDB_client
        self.polling = polling

    def get_inference(self, id: str) -> GetInferenceResponse:
        self.dynamoDB_client.get_table_name(self.polling)
        return GetInferenceResponse(**{"result": self.dynamoDB_client.get_item(key=id)})
