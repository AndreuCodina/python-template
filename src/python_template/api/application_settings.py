from pathlib import Path

from azure.identity import DefaultAzureCredential
from pydantic import Field, SecretStr
from pydantic_settings import (
    AzureKeyVaultSettingsSource,
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from python_template.common.application_environment import ApplicationEnvironment

current_path = Path(__file__).parent.resolve()


class ApplicationSettings(BaseSettings):
    logging_level: str
    cosmos_db_no_sql_url: str
    cosmos_db_no_sql_key: SecretStr = Field(alias="CosmosDbNoSqlKey")
    cosmos_db_no_sql_database: str

    model_config = SettingsConfigDict(
        extra="ignore",
        env_nested_delimiter="__",
        env_file=(
            str(current_path / ".env"),
            str(current_path / f".env.{ApplicationEnvironment.get_current()}"),
        ),
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        settings = (init_settings, env_settings, dotenv_settings, file_secret_settings)

        if ApplicationEnvironment.get_current() != ApplicationEnvironment.LOCAL:
            azure_key_vault = AzureKeyVaultSettingsSource(
                settings_cls,
                dotenv_settings()["key_vault_url"],
                DefaultAzureCredential(),
            )
            settings = (azure_key_vault, *settings)

        return settings
