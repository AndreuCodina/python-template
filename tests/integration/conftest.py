import pytest

from python_archetype.api.dependency_container import DependencyContainer


@pytest.fixture(autouse=True)
async def initialize_dependency_container() -> None:
    await DependencyContainer.initialize()
