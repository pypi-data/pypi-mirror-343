import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
    retry_if_exception_type,
    RetryError
)
from typing import Any, Optional, Type


class RetryMixin:
    """
    Миксин для повторной попытки выполнения запроса.
    """

    def __init__(self, max_retries: int = 3, wait_time: int = 2):
        """
        Инициализация миксина.
        :param max_retries: Максимальное количество попыток.
        :param wait_time: Время ожидания между попытками.
        """

        self.max_retries = max_retries
        self.wait_time = wait_time

    retry_exceptions: Optional[tuple[Type[BaseException], ...]] = (
        httpx.HTTPStatusError,
        httpx.NetworkError,
        httpx.TimeoutException,
        httpx.TooManyRedirects,
        httpx.RequestError,
        httpx.ConnectTimeout,
        httpx.ReadTimeout,
        RetryError
    )

    def _get_retry_decorator(self) -> Any:
        """
        Возвращает декоратор для повторной попытки выполнения запроса.
        :return: Декоратор.
        """

        return retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_fixed(self.wait_time),
            retry=retry_if_exception_type(self.retry_exceptions),
            reraise=True
        )

    def with_retry(self, func: Any) -> Any:
        """
        Оборачивает функцию в декоратора повторной попытки.
        :param func: Функция, которую нужно обернуть.
        :return: Обернутая функция.
        """

        return self._get_retry_decorator()(func)

    async def fetch_with_retry(self, fetch_fn: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Выполняет запрос с повторной попыткой.
        :param fetch_fn: Функция для выполнения запроса.
        :param args: Аргументы для функции.
        :param kwargs: Ключевые аргументы для функции.
        :return: Результат выполнения функции.
        """

        retry_func = self._get_retry_decorator()(fetch_fn)
        try:
            return await retry_func(*args, **kwargs)
        except RetryError as e:
            raise e.last_attempt.exception()
