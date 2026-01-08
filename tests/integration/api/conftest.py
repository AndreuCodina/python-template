from collections.abc import AsyncGenerator

import pytest
from aspy_dependency_injection.service_provider import ServiceProvider
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from python_template.api.main import configure_services, create_app
from python_template.api.services.email_service import EmailService


@pytest.fixture(autouse=True)
async def test_client() -> AsyncGenerator[TestClient]:
    with TestClient(create_app()) as test_client:
        yield test_client


@pytest.fixture
async def service_provider(mocker: MockerFixture) -> AsyncGenerator[ServiceProvider]:
    services = configure_services()
    email_service_mock = mocker.create_autospec(EmailService, instance=True)
    services.add_transient(EmailService, email_service_mock)
    async with services.build_service_provider() as service_provider:
        yield service_provider
