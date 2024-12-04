import logging
from typing import Dict

import boto3

from app.core.config import settings

_logger = logging.getLogger(f"custom.{__name__}")


class DynamoDB_Client:
    def __init__(self) -> None:
        if settings.ENVIRONMENT == "local":
            self.client = boto3.client("dynamodb", endpoint_url="http://dynamodb:8000")
            _logger.info("DynamoDB local endpoint")
        else:
            self.client = boto3.client("dynamodb")

    def get_table_name(self, polling: bool) -> str:
        return (
            settings.DYNAMO_DB_POLING_TABLE
            if polling
            else settings.DYNAMO_DB_PUSH_TABLE
        )

    def put_item(self, table_name: str, item: Dict) -> None:
        _logger.info(item)
        self.client.put_item(TableName=table_name, Item=item)
