from collections.abc import AsyncGenerator

import pytest
from azure.cosmos.aio import CosmosClient, DatabaseProxy

from api.dependency_container import DependencyContainer


@pytest.fixture(autouse=True)
def initialize_dependency_container() -> None:
    DependencyContainer.initialize()


@pytest.fixture
async def cosmosdb_database() -> AsyncGenerator[DatabaseProxy, None]:
    application_settings = DependencyContainer.get_application_settings()

    async with CosmosClient(
        application_settings.cosmos_db_no_sql_url,
        application_settings.cosmos_db_no_sql_key.get_secret_value(),
    ) as cosmosdb_client:
        cosmosdb_database = cosmosdb_client.get_database_client(
            application_settings.cosmos_db_no_sql_database
        )
        yield cosmosdb_database
