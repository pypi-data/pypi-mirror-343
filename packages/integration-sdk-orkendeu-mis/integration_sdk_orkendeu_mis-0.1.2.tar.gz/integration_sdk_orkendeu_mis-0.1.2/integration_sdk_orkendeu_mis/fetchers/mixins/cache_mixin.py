import hashlib
import json

from typing import Any, Dict, Optional
from aioredis import Redis


class RedisCacheMixin:
    redis_client: Redis
    cache_ttl: int = 300

    def _generate_cache_key(self, data: Dict[str, Any], prefix: str = "cache") -> str:
        """
        Генерирует ключ для кеша на основе данных и префикса.
        :param data: Данные, которые будут использоваться для генерации ключа.
        :param prefix: Префикс для ключа.
        :return: Ключ для кеша.
        """

        raw = json.dumps(data, sort_keys=True)
        hashed = hashlib.md5(raw.encode()).hexdigest()
        return f"{prefix}:{hashed}"

    async def get_from_cache(self, data: Dict[str, Any], prefix: str = "cache") -> Optional[Dict[str, Any]]:
        """
        Получает данные из кеша.
        :param data: Данные, которые будут использоваться для генерации ключа.
        :param prefix: Префикс для ключа.
        :return: Данные из кеша или None, если данных нет.
        """

        key = self._generate_cache_key(data, prefix)
        cached_data = await self.redis_client.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None

    async def set_to_cache(self, data: Dict[str, Any], response: bytes, prefix: str = "cache") -> None:
        """
        Сохраняет данные в кеш.
        :param data: Данные, которые будут использоваться для генерации ключа.
        :param response: Данные, которые будут сохранены в кеш.
        :param prefix: Префикс для ключа.
        :return: None
        """

        key = self._generate_cache_key(data, prefix)
        await self.redis_client.set(key, response, ex=self.cache_ttl)

    async def clear_cache(self, data: Dict[str, Any], prefix: str = "cache") -> None:
        """
        Очищает кеш для заданных данных.
        :param data: Данные, которые будут использоваться для генерации ключа.
        :param prefix: Префикс для ключа.
        :return: None
        """

        key = self._generate_cache_key(data, prefix)
        await self.redis_client.delete(key)

    async def clear_all_cache(self, prefix: str = "cache") -> None:
        """
        Очищает весь кеш с заданным префиксом.
        :param prefix: Префикс для ключа.
        :return: None
        """

        keys = await self.redis_client.keys(f"{prefix}:*")
        if keys:
            await self.redis_client.delete(*keys)
