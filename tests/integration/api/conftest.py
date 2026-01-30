from collections.abc import AsyncGenerator

import pytest
from wirio.service_container import ServiceContainer

from python_template.api.main import services


@pytest.fixture
async def services_fixture() -> AsyncGenerator[ServiceContainer]:
    async with services:
        yield services
