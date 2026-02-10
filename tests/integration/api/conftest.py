from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from wirio.integrations.fastapi import get_service_provider
from wirio.service_provider import ServiceProvider

from python_template.api.main import app


@pytest.fixture
def service_provider() -> Generator[ServiceProvider]:
    with TestClient(app):
        yield get_service_provider(app)
