import json
import logging
from datetime import datetime
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
        self.table.put_item(Item=item)

    def batch_put_item(self, data_list: List[DynamoDBData]) -> None:
        with self.table.batch_writer() as batch:
            for data in data_list:
                item = self._convert_from_dynamodb_data(data)
                batch.put_item(Item=item)

    def get_item(self, key: str) -> DynamoDBData:
        response = self.table.get_item(Key={"id": key})
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
        return DynamoDBData(
            id=item["id"],
            group_id=item["group_id"],
            group_index=int(item["group_index"]),
            system=item["system"],
            status=item["status"],
            model=item["model"],
            path=item["path"],
            input=json.loads(item["input"]),
            result=json.loads(item["result"]),
            create_at=datetime.fromisoformat(item["create_at"]),
            update_at=datetime.fromisoformat(item["update_at"]),
        )
