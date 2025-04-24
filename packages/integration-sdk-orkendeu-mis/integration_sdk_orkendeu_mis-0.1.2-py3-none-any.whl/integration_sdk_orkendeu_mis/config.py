import logging

from integration_sdk_orkendeu_mis.settings import settings


def setup_logger() -> logging.Logger:
    """
    Настройка логгера для интеграционного SDK.
    :return: Логгер.
    """
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format=settings.LOG_FORMAT,
    )
    logger = logging.getLogger("integration_sdk_orkendeu_mis")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    return logger


logger = setup_logger()
