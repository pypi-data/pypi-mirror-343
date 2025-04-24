import httpx
from typing import Any, Dict, Optional
from urllib.parse import urljoin

from integration_sdk_orkendeu_mis.fetchers.abstract import AbstractFetcher


class SyncRESTFetcher(AbstractFetcher):
    """
    REST фетчер. Использует JSON-payload.
    """

    method: str = "GET"
    content_type: str = "application/json"

    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
        self.url = url
        self.headers = headers or {}

    @staticmethod
    def get_url(base_url: str, base_path: str = "") -> str:
        """
        Метод для получения URL.
        :param base_url: Базовый URL.
        :param base_path: Базовый путь.
        :return: URL.
        """

        return urljoin(base_url, base_path)

    def build_payload(self, validated_data: Dict[str, Any]) -> Any:
        """
        Метод для сборки payload.
        :param validated_data: Данные, которые были проверены.
        :return: Payload.
        """

        return validated_data.get("data", {})

    async def fetch(self, validated_data: Dict[str, Any], **kwargs: Any) -> bytes:
        """
        Метод для получения данных.
        :param validated_data: Данные, которые были проверены.
        :param kwargs: Дополнительные параметры.
        :return: Полученные данные.
        """

        base_url = validated_data.get("base_url", self.url)
        base_path = validated_data.get("base_path", "")
        timeout = validated_data.get("timeout", 10)

        url = self.get_url(base_url, base_path)
        payload = self.build_payload(validated_data)
        headers = self.set_headers(self.headers, **kwargs)
        auth = await self.get_auth(**validated_data)

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=self.method,
                url=url,
                headers=headers,
                timeout=timeout,
                auth=auth,
                json=payload if self.method in ["POST", "PUT", "PATCH"] else None,
                params=payload if self.method in ["GET", "DELETE"] else None,
            )

        response.raise_for_status()
        return response.content
