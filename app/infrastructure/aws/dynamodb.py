import json
import logging
from typing import Dict, List

import boto3

from app.core.config import settings
from app.domain.entities.dynamodb_entity import DynamoDBData

_logger = logging.getLogger(f"custom.{__name__}")


class DynamoDB_Client:
    def __init__(self) -> None:
        if settings.ENVIRONMENT == "local":
            self.resource = boto3.resource(
                "dynamodb", endpoint_url="http://dynamodb:8000"
            )
            _logger.info("DynamoDB local endpoint")
        else:
            self.client = boto3.resource("dynamodb")

    def get_table_name(self, polling: bool) -> None:
        self.table = self.resource.Table(  # type: ignore
            settings.DYNAMO_DB_POLING_TABLE
            if polling
            else settings.DYNAMO_DB_PUSH_TABLE
        )

    def put_item(self, data: DynamoDBData) -> None:
        item = self._convert_from_dynamodb_data(data)
        _logger.info(item)
        self.table.put_item(Item=item)

    def batch_put_item(self, data_list: List[DynamoDBData]) -> None:
        with self.table.batch_writer() as batch:
            for data in data_list:
                item = self._convert_from_dynamodb_data(data)
                _logger.info(item)
                batch.put_item(Item=item)

    def get_item(self, key: str) -> DynamoDBData:
        response = self.table.get_item(Key={"id": {"S": key}})
        return self._convert_to_dynamodb_data(response)

    def _convert_from_dynamodb_data(self, item: DynamoDBData) -> Dict:
        return {
            "id": item.id,
            "group_id": item.group_id,
            "group_index": str(item.group_index),
            "system": item.system.value,
            "status": item.status.value,
            "model": item.model.value,
            "path": item.path,
            "input": json.dumps(item.input),
            "result": json.dumps(item.result),
            "create_at": item.create_at.isoformat(),
            "update_at": item.update_at.isoformat(),
        }

    def _convert_to_dynamodb_data(self, response: Dict) -> DynamoDBData:
        item = response["Item"]
        _logger.info(item)
        return DynamoDBData(
            id=item["id"]["S"],
            group_id=item["group_id"]["S"],
            group_index=int(item["group_index"]["N"]),
            system=item["system"]["S"],
            status=item["status"]["S"],
            model=item["model"]["S"],
            path=item["path"]["S"],
            input=json.loads(item["input"]["S"]),
            result=json.loads(item["result"]["S"]),
            create_at=item["request_date"]["S"],
            update_at=item["response_date"]["S"],
        )
