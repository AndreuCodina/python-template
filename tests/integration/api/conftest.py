from collections.abc import AsyncGenerator

import pytest
from wirio.service_provider import ServiceProvider

from python_template.api.main import services


@pytest.fixture
async def service_provider() -> AsyncGenerator[ServiceProvider]:
    async with services.build_service_provider() as service_provider:
        yield service_provider
