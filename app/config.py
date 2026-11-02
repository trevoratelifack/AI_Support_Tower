from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Operation control tower"
    app_version: str = "0.1.0"
    app_description: str = "AI Operation Control Tower"
    app_env: str = "development"
    log_level: str = "INFO"
    model_name: str = "gpt-4o-mini"
    openai_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
    