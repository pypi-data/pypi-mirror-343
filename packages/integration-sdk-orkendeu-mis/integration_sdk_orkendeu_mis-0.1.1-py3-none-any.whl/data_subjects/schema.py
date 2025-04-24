from typing import Any, List, Optional, Literal

from pydantic import BaseModel, Extra
from pydantic.json import pydantic_encoder


ParamLiteral = Literal[
    "INT", "FLOAT", "STRING", "BASE64", "BOOL", "URL", "CHOICE", "JSON",
    "UUID", "DATE", "DATETIME", "FILE", "UNDEFINED"
]


class ParamSchema(BaseModel):
    """
    Схема параметра.
    """
    label: str
    name: str
    type: ParamLiteral
    default_value: Optional[Any] = None
    required: bool = False
    description: Optional[str] = None
    choices: Optional[List[str]] = None
    example: Optional[Any] = None

    class Config:
        """
        Конфигурация модели.
        """
        extra = Extra.forbid
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {
            ParamLiteral: lambda v: v.value,
            Any: lambda v: pydantic_encoder(v),
        }
        schema_extra = {
            "example": {
                "label": "Метод",
                "name": "method",
                "type": "CHOICE",
                "required": True,
                "default_value": "GET",
                "description": "Метод запроса",
                "choices": ["GET", "POST", "PUT", "DELETE"],
                "example": "GET"
            }
        }


class UndefinedSchema(BaseModel):
    """
    Схема для неопределенных параметров.
    """
    detail: str
    type: Literal["UNDEFINED"] = "UNDEFINED"

    class Config:
        """
        Конфигурация модели.
        """
        extra = Extra.forbid
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {
            ParamLiteral: lambda v: v.value,
            Any: lambda v: pydantic_encoder(v),
        }
        schema_extra = {
            "example": {
                "detail": "This is an undefined schema"
            }
        }
