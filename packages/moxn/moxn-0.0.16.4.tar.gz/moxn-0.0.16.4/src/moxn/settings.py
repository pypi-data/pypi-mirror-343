from pydantic import HttpUrl, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class MoxnSettings(BaseSettings):
    """Configuration settings for the Moxn client."""

    user_id: str
    org_id: str | None = None
    api_key: SecretStr
    base_api_route: HttpUrl = Field(
        default=HttpUrl("https://marksweissma--moxn-api-fastapi-app.modal.run")
    )
    timeout: float = Field(default=60.0, description="Prompt timeout in seconds")

    model_config = SettingsConfigDict(
        frozen=True,
        extra="forbid",
        env_file=[".env.local", ".env"],
        env_prefix="MOXN_",
        env_file_encoding="utf-8",
    )
