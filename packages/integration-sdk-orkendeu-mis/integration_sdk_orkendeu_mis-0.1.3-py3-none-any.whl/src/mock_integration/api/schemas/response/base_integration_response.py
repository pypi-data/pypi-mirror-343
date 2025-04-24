from typing import Any, Dict, List, Optional, Union, Tuple
from pydantic import BaseModel, Field, Extra

from src.mock_integration.data_subjects.get_person_info_subject import GetPersonInfoMockResponseSchema


class BaseIntegrationResponse(BaseModel):
    """
    Базовый класс для всех ответов интеграции.
    """

    success: bool = Field(
        default=True,
        description="Флаг успешности выполнения интеграции",
    )
    data: Union[
        GetPersonInfoMockResponseSchema,
        Dict[str, Any],
        str,
    ] = Field(
        default=GetPersonInfoMockResponseSchema,
        description="Данные ответа интеграции",
    )
    error: Optional[Union[str, Dict[str, Any]]] = Field(
        default=None,
        description="Ошибка, если интеграция завершилась неуспешно",
    )
    status_code: int = Field(
        default=200,
        description="HTTP статус код ответа интеграции",
    )
