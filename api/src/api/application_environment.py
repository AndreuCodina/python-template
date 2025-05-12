import os
from enum import StrEnum


class ApplicationEnvironment(StrEnum):
    LOCAL = "Local"
    DEVELOPMENT = "Development"
    STAGING = "Staging"
    PRODUCTION = "Production"

    @staticmethod
    def get_current() -> str:
        return os.getenv("COMMON__ENVIRONMENT", ApplicationEnvironment.LOCAL)
