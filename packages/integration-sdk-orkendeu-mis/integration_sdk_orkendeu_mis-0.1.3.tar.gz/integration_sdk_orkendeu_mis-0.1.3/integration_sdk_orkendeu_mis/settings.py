from pydantic.v1 import BaseSettings


class SDKSettings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    ENV: str = "dev"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = SDKSettings()
