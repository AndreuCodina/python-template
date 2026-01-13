from collections.abc import AsyncGenerator

import pytest
from aspy_dependency_injection.service_provider import ServiceProvider
from pytest_mock import MockerFixture

from python_template.api.main import services
from python_template.api.services.email_service import EmailService


@pytest.fixture
async def service_provider(mocker: MockerFixture) -> AsyncGenerator[ServiceProvider]:
    email_service_mock = mocker.create_autospec(EmailService, instance=True)
    services.add_singleton(EmailService, email_service_mock)

    async with services.build_service_provider() as service_provider:
        yield service_provider
