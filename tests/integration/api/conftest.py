from collections.abc import AsyncGenerator

import pytest
from aspy_dependency_injection.service_provider import ServiceProvider

from python_template.api.main import configure_services


@pytest.fixture
async def service_provider() -> AsyncGenerator[ServiceProvider]:
    services = configure_services()

    async with services.build_service_provider() as service_provider:
        yield service_provider
