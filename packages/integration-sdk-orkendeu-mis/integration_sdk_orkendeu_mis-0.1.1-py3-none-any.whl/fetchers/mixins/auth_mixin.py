from typing import Any, Optional, Tuple


class BasicAuthMixin:
    """
    Миксин для базовой аутентификации.
    """

    def __init__(self, username: str, password: str):
        """
        Инициализация базовой аутентификации.

        :param username: Username для базовой аутентификации.
        :param password: Password для базовой аутентификации.
        """

        self.username = username
        self.password = password

    async def get_auth(self, **kwargs: Any) -> Optional[Tuple[str, str]]:
        """
        Возвращает кортеж с именем пользователя и паролем для базовой аутентификации.

        :return: Кортеж с именем пользователя и паролем.
        """

        return self.username, self.password