from integration_sdk_orkendeu_mis.providers.abstract import AbstractProvider


class GetPersonInfoMockProvider(AbstractProvider):
    code = "GET_PERSON_INFO"
    label = "Получить информацию о человеке по номеру телефона"
    description = "Получить информацию о человеке по номеру телефона"
    params = []
