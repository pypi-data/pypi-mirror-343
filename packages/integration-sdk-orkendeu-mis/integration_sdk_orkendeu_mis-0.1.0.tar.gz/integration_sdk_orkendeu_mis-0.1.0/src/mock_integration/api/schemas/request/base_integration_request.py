from typing import Any, Dict, Optional, Union, List, Tuple
from pydantic import BaseModel, Field

from src.mock_integration.data_subjects.get_person_info_subject import GetPersonInfoMockPayloadSchema


class BaseIntegrationRequest(BaseModel):
    """
    Базовый класс для запросов интеграции.
    """
    payload: Union[GetPersonInfoMockPayloadSchema, Dict[str, Any]] = Field(
        default=GetPersonInfoMockPayloadSchema,
        description="Данные запроса интеграции",
    )
