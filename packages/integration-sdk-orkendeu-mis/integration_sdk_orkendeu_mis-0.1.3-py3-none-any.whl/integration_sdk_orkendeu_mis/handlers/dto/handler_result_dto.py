from typing import Any, Dict, Optional, Union, List
from pydantic import BaseModel, Field


class HandlerResultDTO(BaseModel):
    """
    DTO для результата обработки данных в handler.
    """

    success: bool = Field(
        default=True,
        description="Успешность выполнения операции",
    )
    data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = Field(
        default=None,
        description="Данные, возвращаемые handler'ом",
    )
    error: Optional[str] = Field(
        default=None,
        description="Ошибка, возникшая при выполнении операции",
    )
    status_code: int = Field(
        default=200,
        description="HTTP статус код",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Метаданные, связанные с результатом",
    )
