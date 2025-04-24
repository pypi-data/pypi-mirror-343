from typing import Any, Dict
from pydantic import ValidationError

from integration_sdk_orkendeu_mis.data_subjects.abstract import AbstractDataSubject


class ValidationMixin:
    data_subject: AbstractDataSubject

    def validate_payload(self, payload: Dict[str, Any]) -> None:
        """
        Метод для валидации payload.
        :param payload: Данные, которые нужно проверить.
        :return: Кортеж из булевого значения и словаря с ошибками.
        """

        if not self.data_subject:
            return

        try:
            self.data_subject.payload_schema(**payload)
        except ValidationError as e:
            raise ValueError(f"Payload validation error: {e}")

    def validate_response(self, response: Any) -> None:
        """
        Метод для валидации ответа.
        :param response: Ответ, который нужно проверить.
        :return: Кортеж из булевого значения и словаря с ошибками.
        """

        if not self.data_subject or not self.data_subject.response_schema:
            return

        try:
            self.data_subject.response_schema(**response)
        except ValidationError as e:
            raise ValueError(f"Response validation error: {e}")
