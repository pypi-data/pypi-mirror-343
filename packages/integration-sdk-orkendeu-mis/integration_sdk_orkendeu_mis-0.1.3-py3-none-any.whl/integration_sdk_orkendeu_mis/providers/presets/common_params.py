from integration_sdk_orkendeu_mis.data_subjects.schema import ParamSchema


USERNAME_PARAM = ParamSchema(
    label="Имя пользователя",
    name="username",
    type="STRING",
    default_value=None,
    required=True,
    description="Имя пользователя для доступа к API",
    choices=["admin", "user", "guest"],
    example="admin",
)

PASSWORD_PARAM = ParamSchema(
    label="Пароль",
    name="password",
    type="STRING",
    default_value=None,
    required=True,
    description="Пароль для доступа к API",
    choices=["admin123", "user123", "guest123"],
    example="admin123",
)

TOKEN_PARAM = ParamSchema(
    label="Токен доступа",
    name="token",
    type="STRING",
    default_value=None,
    required=True,
    description="Токен доступа к API",
    choices=["token"],
    example="token",
)