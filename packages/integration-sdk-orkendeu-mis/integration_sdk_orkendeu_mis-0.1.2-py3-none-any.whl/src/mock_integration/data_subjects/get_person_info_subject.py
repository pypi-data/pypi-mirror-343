from abc import ABC

from pydantic import BaseModel, Field

from integration_sdk_orkendeu_mis.data_subjects.abstract import AbstractDataSubject


class GetPersonInfoMockPayloadSchema(BaseModel):
    phone_number: str = Field(
        ...,
        description="Номер телефона человека",
    )


class GetPersonInfoMockResponseSchema(BaseModel):
    phone_number: str = Field(
        ...,
        description="Номер телефона человека",
    )
    full_name: str = Field(
        ...,
        description="ФИО человека",
    )
    iin: str = Field(
        ...,
        description="ИИН человека",
    )


class GetPersonInfoMockSubject(AbstractDataSubject, ABC):
    code = "GET_PERSON_INFO"
    label = "Получить информацию о человеке по номеру телефона"
    payload_schema = GetPersonInfoMockPayloadSchema
    response_schema = GetPersonInfoMockResponseSchema