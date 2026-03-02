from pydantic import BaseModel


class ApplicationSettings(BaseModel):
    logging_level: str
    key_vault_url: str
    application_insights_connection_string: str
    postgresql_connection_string: str
