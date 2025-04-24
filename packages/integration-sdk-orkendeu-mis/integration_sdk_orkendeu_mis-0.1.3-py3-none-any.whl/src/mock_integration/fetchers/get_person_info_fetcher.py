import json
from abc import ABC
from typing import Dict, Any

from integration_sdk_orkendeu_mis.fetchers.abstract import AbstractFetcher


MOCK_USERS = {
    "+77076098760": {
        "full_name": "Anvarbek Nurzhauganov",
        "phone_number": "+777076098760",
        "iin": "030611550511"
    },
    "+77083531419": {
        "full_name": "Igor Ruzhilov",
        "phone_number": "+77083531419",
        "iin": "005869551365"
    },
    "+77777617874": {
        "full_name": "Vlad Andreev",
        "phone_number": "+77777617874",
        "iin": "008965556325"
    },
}


class GetPersonInfoMockFetcher(AbstractFetcher, ABC):
    """
    Фетчер для получения информации о человеке по номеру телефона.
    Использует JSON-payload.
    """

    async def fetch(self, validated_data: Dict[str, Any], **kwargs: Any) -> Any:
        phone_number = validated_data.get("phone_number")
        user_data = MOCK_USERS.get(phone_number)

        if not user_data:
            return json.dumps({
                "error": f"User with phone number {phone_number} not found",
                "status_code": 404
            }).encode()

        return json.dumps(user_data).encode()
