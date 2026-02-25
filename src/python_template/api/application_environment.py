import os
from enum import StrEnum, auto


class ApplicationEnvironment(StrEnum):
    LOCAL = auto()
    DEVELOPMENT = auto()
    STAGING = auto()
    PRODUCTION = auto()

    @staticmethod
    def get_current() -> str:
        return os.getenv("PYTHON_APP_ENVIRONMENT", ApplicationEnvironment.LOCAL)
