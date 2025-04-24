from abc import ABC
from typing import Any, Dict, Optional, Type

from integration_sdk_orkendeu_mis.data_subjects.abstract import AbstractDataSubject
from integration_sdk_orkendeu_mis.fetchers.abstract import AbstractFetcher
from integration_sdk_orkendeu_mis.handlers.dto.handler_result_dto import HandlerResultDTO
from integration_sdk_orkendeu_mis.handlers.mixins.trace_logging import TraceLoggingMixin
from integration_sdk_orkendeu_mis.handlers.mixins.validation import ValidationMixin
from integration_sdk_orkendeu_mis.parsers.abstract import AbstractParser
from integration_sdk_orkendeu_mis.parsers.mixins.error_check import ParserError
from integration_sdk_orkendeu_mis.providers.abstract import AbstractProvider


class AbstractServiceHandler(ValidationMixin, ABC):
    """
    Главный обработчик. Соединяет все части интеграции.
    """

    fetcher_class: Type[AbstractFetcher]
    parser_class: Type[AbstractParser]
    provider_class: Type[AbstractProvider]
    data_subject_class: Type[AbstractDataSubject]

    call_back_handler_class: Optional[Type] = None

    def __init__(self):
        self.fetcher = self.fetcher_class()
        self.parser = self.parser_class()
        self.provider = self.provider_class()
        self.data_subject = self.data_subject_class()
        self.trace_logger = TraceLoggingMixin()

    async def handle(self, payload: Dict[str, Any], **kwargs: Any) -> HandlerResultDTO:
        """
        Метод для обработки запроса.
        :param payload: Данные, которые нужно обработать.
        :param kwargs: Дополнительные параметры.
        :return: Результат обработки.
        """

        try:
            self.trace_logger.log_trace("validate_payload", "Начало валидации", payload)
            self.validate_payload(payload)

            self.trace_logger.log_trace("fetch", "Отправка запроса во внешний сервис")
            raw = await self.fetcher.fetch(payload)

            self.trace_logger.log_trace("parse", "Парсинг ответа")
            parsed = self.parser(raw)

            self.trace_logger.log_success(parsed)
            self.validate_response(parsed)

            return HandlerResultDTO(success=True, data=parsed)

        except ParserError as e:
            self.trace_logger.log_error(e)
            return HandlerResultDTO(success=False, error=f"Parser error: {e}", status_code=400)
        except Exception as e:
            self.trace_logger.log_error(e)
            return HandlerResultDTO(success=False, error=f"Handler failed: {e}", status_code=403)
