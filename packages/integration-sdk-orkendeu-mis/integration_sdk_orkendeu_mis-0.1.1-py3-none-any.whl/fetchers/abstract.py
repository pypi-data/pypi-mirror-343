from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class AbstractFetcher(ABC):
    """
    Абстрактный класс для всех классов, которые будут использоваться в качестве Fetcher.
    """

    @abstractmethod
    async def fetch(self, validated_data: Dict[str, Any], **kwargs: Any) -> Any:
        """
        Метод для получения данных.
        :param validated_data: Данные, которые были проверены.
        :param kwargs: Дополнительные параметры.
        :return: Полученные данные.
        """

        pass

    @staticmethod
    def get_headers(**kwargs: Any) -> Dict[str, str]:
        """
        Метод для получения заголовков.
        :param kwargs: Дополнительные параметры.
        :return: Заголовки.
        """

        return {}

    def set_headers(self, custom_headers: Dict[str, str], **kwargs: Any) -> Dict[str, str]:
        """
        Метод для установки заголовков.
        :param custom_headers: Заголовки.
        :param kwargs: Дополнительные параметры.
        :return: Заголовки.
        """

        base = self.get_headers()
        base.update(custom_headers)
        return base

    @staticmethod
    async def get_auth(**kwargs: Any) -> Optional[Dict[str, str]]:
        """
        Метод для получения аутентификации.
        :param kwargs: Дополнительные параметры.
        :return: Аутентификация.
        """

        return None