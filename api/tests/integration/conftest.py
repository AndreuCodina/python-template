import pytest

from api.dependency_container import DependencyContainer


@pytest.fixture(autouse=True)
def initialize_dependency_container() -> None:
    DependencyContainer.initialize()
