from abc import ABC

from src.integration_sdk.providers.abstract import AbstractProvider


class GetPersonInfoMockProvider(AbstractProvider):
    code = "GET_PERSON_INFO"
    label = "Получить информацию о человеке по номеру телефона"
    description = "Получить информацию о человеке по номеру телефона"
    params = []
