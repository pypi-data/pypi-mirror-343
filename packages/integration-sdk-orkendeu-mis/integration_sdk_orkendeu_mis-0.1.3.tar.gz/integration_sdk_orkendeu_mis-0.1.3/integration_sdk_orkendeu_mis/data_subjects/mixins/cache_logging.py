import logging
from typing import Optional, List


class CacheLoggingMixin:
    """
    Миксин для кэширования и логирования запросов и ответов интеграции.
    """
    allow_cache: bool = False
    cache_key_fields: Optional[List[str]] = None
    enable_logging: bool = True

    def __init__(self, logger: Optional[object] = None):
        self.logger = logger or self.get_default_logger()

    @staticmethod
    def get_default_logger() -> logging.Logger:
        """
        Метод для получения логгера по умолчанию.
        :return: Логгер.
        """

        import logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def get_cache_key(self, payload: dict) -> Optional[str]:
        """
        Метод для получения ключа кэша.
        :param payload: Данные, которые были проверены.
        :return: Ключ кэша.
        """

        if not self.allow_cache or not self.cache_key_fields:
            return None
        try:
            return "_".join([str(payload[k]) for k in self.cache_key_fields])
        except KeyError:
            return None

    def log_request(self, message: str) -> None:
        """
        Метод для логирования запроса.
        :param message: Сообщение для логирования.
        :return: None
        """

        if self.enable_logging:
            self.logger.info(message)
