import logging

from boto3 import client

from app.core.config import settings

_logger = logging.getLogger(f"custom.{__name__}")


# sqs用のクラスを作成
class SQS_Client:
    def __init__(self) -> None:
        # 環境変数ENVIRONMENTがlocalの場合はエンドポイントを指定してSQSクライアントを作成
        if settings.ENVIRONMENT == "local":
            self.client = client("sqs", endpoint_url="http://sqs:9324")
            _logger.info("SQS local endpoint")
        # それ以外の場合はエンドポイントを指定せずにSQSクライアントを作成
        else:
            self.client = client("sqs")

    # メッセージを送信
    def send_message(self, queue_name: str, message: str) -> None:
        _logger.info(message)
        self.client.send_message(QueueUrl=queue_name, MessageBody=message)  # type: ignore
