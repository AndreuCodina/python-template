from collections.abc import AsyncGenerator

import pytest

from python_seed.api.dependency_container import DependencyContainer


@pytest.fixture(autouse=True)
async def initialize_dependency_container() -> AsyncGenerator[None]:
    await DependencyContainer.initialize()
    yield
    await DependencyContainer.uninitialize()
