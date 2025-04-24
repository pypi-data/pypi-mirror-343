import logging

from typing import Any


logger = logging.getLogger("integration_sdk_orkendeu_mis")


class TraceLoggingMixin:
    """
    Миксин для логирования шагов выполнения интеграции.
    """
    enable_trace: bool = True

    def log_trace(self, step: str, message: str = "", payload: Any = None) -> None:
        """
        Метод для логирования шагов выполнения.
        :param step: Шаг выполнения.
        :param message: Сообщение для логирования.
        :param payload: Данные, которые нужно залогировать.
        """
        if not self.enable_trace:
            return

        log_message = f"[TRACE] Step: {step}"
        if message:
            log_message += f" | {message}"
        if payload:
            log_message += f" | Data: {repr(payload)[:300]}"
        logger.info(log_message)

    def log_success(self, data: Any) -> None:
        """
        Метод для логирования успешного выполнения.
        :param data: Данные, которые нужно залогировать.
        """
        if self.enable_trace:
            log_message = f"[SUCCESS] Handler finished. Output: {repr(data)[:500]}"
            logger.info(log_message)

    def log_error(self, error: Exception) -> None:
        """
        Метод для логирования ошибки.
        :param error: Ошибка, которую нужно залогировать.
        """
        if self.enable_trace:
            log_message = f"[ERROR] {type(error).__name__}: {error}"
            logger.error(log_message)
