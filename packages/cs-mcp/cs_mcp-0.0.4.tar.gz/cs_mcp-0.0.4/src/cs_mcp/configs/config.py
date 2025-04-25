from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    IS_DEBUG: bool = False

    class Config:
        env_file = ".env"


config = Settings()
