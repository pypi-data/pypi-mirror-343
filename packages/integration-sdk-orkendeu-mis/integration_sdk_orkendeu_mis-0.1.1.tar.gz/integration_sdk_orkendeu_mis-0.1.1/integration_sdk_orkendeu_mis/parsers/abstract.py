from abc import ABC, abstractmethod
from typing import Any, Optional, Union

from integration_sdk_orkendeu_mis.parsers.mixins.error_check import ServiceUnavailableError


class AbstractParser(ABC):
    """
    Абстрактный класс для всех классов, которые будут использоваться в качестве Parser.
    """

    SERVICE_UNAVAILABLE_CODES: list[int] = [503, 504]
    SUBJECT_NOT_FOUND_CODES: list[int] = [404]
    SERVICE_UNAVAILABLE_MESSAGE: str = "Service Unavailable"
    SUBJECT_NOT_FOUND_MESSAGE: str = "Subject Not Found"

    def __init__(self, **kwargs: Any) -> None:
        """
        Инициализация парсера.
        :param kwargs: Дополнительные параметры.
        """

        self.kwargs = kwargs
        self.response: Optional[Union[bytes, str]] = None
        self.parsed_response: Optional[Any] = None

    @abstractmethod
    def parse(self, data_to_parse: bytes) -> Union[dict, list]:
        """
        Метод для парсинга данных.
        :param data_to_parse: Данные, которые нужно распарсить.
        :return: Распарсенные данные в виде словаря или списка.
        """

        pass

    def post_process(self, parsed_response: Union[dict, list]) -> Union[dict, list]:
        """
        Метод для пост-обработки распарсенных данных.
        :param parsed_response: Распарсенные данные.
        :return: Пост-обработанные данные.
        """

        return parsed_response

    def __call__(self, data_to_parse: bytes) -> Union[dict, list]:
        """
        Метод для вызова парсера.
        :param data_to_parse: Данные, которые нужно распарсить.
        :return: Распарсенные данные в виде словаря или списка.
        """

        if not data_to_parse:
            raise ServiceUnavailableError("Empty data to parse")
        self.response = data_to_parse
        raw = self.parse(data_to_parse)
        self.parsed_response = self.post_process(raw)
        return self.parsed_response
