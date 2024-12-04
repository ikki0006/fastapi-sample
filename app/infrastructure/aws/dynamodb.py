import json
import logging
from typing import Dict

from boto3 import client

from app.core.config import settings
from app.domain.entities.dynamodb_entity import DynamoDBData

_logger = logging.getLogger(f"custom.{__name__}")


class DynamoDB_Client:
    def __init__(self) -> None:
        if settings.ENVIRONMENT == "local":
            self.client = client("dynamodb", endpoint_url="http://dynamodb:8000")
            _logger.info("DynamoDB local endpoint")
        else:
            self.client = client("dynamodb")

    def get_table_name(self, polling: bool) -> str:
        return (
            settings.DYNAMO_DB_POLING_TABLE
            if polling
            else settings.DYNAMO_DB_PUSH_TABLE
        )

    def put_item(self, table_name: str, data: DynamoDBData) -> None:
        item = self._convert_from_dynamodb_data(data)
        _logger.info(item)
        self.client.put_item(TableName=table_name, Item=item)  # type: ignore

    def get_item(self, table_name: str, key: str) -> DynamoDBData:
        response = self.client.get_item(TableName=table_name, Key={"id": {"S": key}})
        return self._convert_to_dynamodb_data(response)

    def _convert_from_dynamodb_data(self, item: DynamoDBData) -> Dict:
        return {
            "id": {"S": item.id},
            "status": {"S": item.status.value},
            "model": {"S": str(item.model.value)},
            "path": {"S": item.path},
            "input": {"S": json.dumps(item.input)},
            "result": {"S": json.dumps(item.result)},
        }

    def _convert_to_dynamodb_data(self, response: Dict) -> DynamoDBData:
        item = response["Item"]
        _logger.info(item)
        return DynamoDBData(
            id=item["id"]["S"],
            status=item["status"]["S"],
            model=item["model"]["S"],
            path=item["path"]["S"],
            input=json.loads(item["input"]["S"]),
            result=json.loads(item["result"]["S"]),
        )
