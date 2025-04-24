from abc import ABC
from typing import Any, Optional, Type, List, Dict
from pydantic import BaseModel

from integration_sdk_orkendeu_mis.data_subjects.schema import ParamSchema, UndefinedSchema


class AbstractDataSubject(ABC):
    """
    Абстрактный класс для всех классов, которые будут использоваться в качестве DataSubject.
    Один data subject = один метод внешнего сервиса.
    """

    # Метаданные
    code: str
    label: str
    description: Optional[str] = ""

    # Схемы
    payload_schema: Type[BaseModel]
    response_schema: Type[BaseModel] = UndefinedSchema
    call_back_schema: Type[BaseModel] = UndefinedSchema

    # Поведение
    params: List[ParamSchema] = []
    allow_cache: bool = False
    cache_key_fields: Optional[List[str]] = None
    enable_logging: bool = True
    version: str = "1.0"
    tags: List[str] = []

    # Параметры расширения
    extra_params: Dict[str, Any] = {}
    response_params: Dict[str, Any] = {}
    error_params: Dict[str, Any] = {}

    # Основные методы

    def get_cache_key(self, payload: dict) -> Optional[str]:
        """
        Генерирует ключ для кеширования запроса.
        :param payload: Данные запроса
        :return: Ключ для кеширования
        """

        if not self.allow_cache or not self.cache_key_fields:
            return None
        try:
            return f"{self.code}_" + "_".join([str(payload[k]) for k in self.cache_key_fields])
        except KeyError:
            return None

    def get_versioned_code(self) -> str:
        """
        Возвращает код с версией.
        :return: Код с версией
        """

        return f"{self.code}_v{self.version.replace('.', '_')}"
