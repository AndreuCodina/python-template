from pathlib import Path

from azure.identity import DefaultAzureCredential
from pydantic import SecretStr
from pydantic.alias_generators import to_pascal
from pydantic_settings import (
    AzureKeyVaultSettingsSource,
    BaseSettings,
    DotEnvSettingsSource,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from python_archetype.common.application_environment import ApplicationEnvironment


class ApplicationSettings(BaseSettings):
    model_config = SettingsConfigDict(alias_generator=to_pascal, extra="ignore")

    logging_level: str
    cosmos_db_no_sql_url: str
    cosmos_db_no_sql_key: SecretStr
    cosmos_db_no_sql_database: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        env_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        dotenv_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        file_secret_settings: PydanticBaseSettingsSource,  # noqa: ARG003
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        env = EnvSettingsSource(
            settings_cls,
            env_nested_delimiter="__",
        )
        current_path = Path(__file__).parent.resolve()
        dotenv = DotEnvSettingsSource(
            settings_cls,
            env_file=[
                str(current_path / ".env"),
                str(current_path / f".env.{ApplicationEnvironment.get_current()}"),
            ],
            env_nested_delimiter=":",
            case_sensitive=True,
        )
        settings = (env, dotenv)

        if ApplicationEnvironment.get_current() != ApplicationEnvironment.LOCAL:
            azure_key_vault = AzureKeyVaultSettingsSource(
                settings_cls,
                dotenv()["AzureKeyVaultUrl"],
                DefaultAzureCredential(),
            )
            settings += (azure_key_vault,)

        return settings
