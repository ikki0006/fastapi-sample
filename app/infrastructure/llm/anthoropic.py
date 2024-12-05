import logging
import time

import httpx
from anthropic import Anthropic
from anthropic.types import Message, MessageParam

from app.core.config import settings
from app.core.exception import LLMApiGenerationError
from app.domain.entities.llm_entity import LLMApiResponse
from app.domain.enum.llm_enum import AnthropicModelName, LLMRole

_logger = logging.getLogger(f"custom.{__name__}")


class AnthoropicApi:
    def _select_anthropic_api_key(self) -> str:
        return settings.ANTHROPIC_API_KEY_1

    def generate(
        self,
        model_name: AnthropicModelName,
        message: str,
        temperature: float = 0.0,
        max_tokens: int = 4096,
        top_k: int = 1,
        n_retry: int = 3,
    ) -> LLMApiResponse | None:
        api_key = self._select_anthropic_api_key()
        client = Anthropic(
            api_key=api_key,
            timeout=httpx.Timeout(120.0, read=5.0, write=10.0, connect=2.0),
        )

        response = None
        for idx in range(1, n_retry + 1):
            try:
                _logger.info(f"({idx}/{n_retry}) Generating response...")
                start_time = time.time()
                messages = self._build_messages(message)
                chat_completion = client.messages.create(
                    max_tokens=max_tokens,
                    messages=messages,
                    temperature=temperature,
                    top_k=top_k,
                    model=model_name.value,
                )
                response_time = time.time() - start_time
                _logger.info(f"(response_time: {response_time:.3f} sec)")
                _logger.info(str(chat_completion))
                response = self._rearrange_response(
                    chat_completion, response_time=response_time
                )
                if response is not None:
                    break
            except Exception as err:
                _logger.info(f"({idx}/{n_retry}): {type(err)}: {str(err)}")
                # Anthropic がAPIのエラー型を内部パッケージで持ってるため、importできないのでignoreで無視
                if hasattr(err, "response") and isinstance(
                    err.response,  # type: ignore
                    httpx.Response,
                ):
                    status_code = err.response.status_code  # type: ignore
                    _logger.info(f"status_code: {status_code}")
                time.sleep(2.0**idx)
        if response is None:
            raise LLMApiGenerationError("Failed to generate response.")
        return response

    def _build_messages(self, prompt: str) -> list[MessageParam]:
        return [
            {"role": "user", "content": prompt},
        ]

    def _rearrange_response(
        self, chat_completion: Message, response_time: float
    ) -> LLMApiResponse:
        return LLMApiResponse(
            id=chat_completion.id,
            model=chat_completion.model,
            content=chat_completion.content[0].text,
            role=LLMRole.ASSISTANT,
            input_tokens=chat_completion.usage.input_tokens,
            output_tokens=chat_completion.usage.output_tokens,
        )
