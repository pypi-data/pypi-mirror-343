class ErrorHandlingMixin:
    """
    Миксин для обработки ошибок в интеграции с API.
    """
    def handle_error(self, error: Exception) -> None:
        raise error

    def handle_any_error(self, any_error: Exception) -> None:
        raise any_error

    def handle_exception(self, exception: Exception) -> None:
        raise exception

    def handle_timeout(self, timeout: Exception) -> None:
        raise timeout

    def handle_validation_error(self, validation_error: Exception) -> None:
        raise validation_error

    def handle_connection_error(self, connection_error: Exception) -> None:
        raise connection_error

    def handle_service_error(self, service_error: Exception) -> None:
        raise service_error

    def handle_http_error(self, http_error: Exception) -> None:
        raise http_error

    def handle_authentication_error(self, authentication_error: Exception) -> None:
        raise authentication_error

    def handle_permission_error(self, permission_error: Exception) -> None:
        raise permission_error
