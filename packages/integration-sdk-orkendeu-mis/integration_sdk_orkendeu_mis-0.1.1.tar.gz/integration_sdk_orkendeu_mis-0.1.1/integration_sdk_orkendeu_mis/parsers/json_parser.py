import json
from typing import Union

from integration_sdk_orkendeu_mis.parsers.abstract import AbstractParser
from integration_sdk_orkendeu_mis.parsers.mixins.error_check import ServiceUnavailableError, ServerUnknownError


class JSONParser(AbstractParser):
    """
    Парсер JSON-ответов от REST-сервисов.
    """

    def parse(self, data_to_parse: bytes) -> Union[dict, list]:
        """
        Метод для парсинга JSON-ответов.
        :param data_to_parse: Данные, которые нужно распарсить.
        :return: Распарсенные данные в виде словаря или списка.
        """

        if not data_to_parse:
            raise ServiceUnavailableError("Empty response")

        try:
            result = json.loads(data_to_parse)
        except json.JSONDecodeError as e:
            raise ServerUnknownError(f"Invalid JSON: {e}", data=data_to_parse)

        if isinstance(result, dict) and result.get("status") in self.SERVICE_UNAVAILABLE_CODES:
            raise ServiceUnavailableError(result.get("message", "Service unavailable"))

        return result