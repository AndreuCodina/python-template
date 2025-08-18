from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from azure.cosmos import PartitionKey
from azure.cosmos.aio import CosmosClient, DatabaseProxy

from api.application_settings import ApplicationSettings
from api.workflows.products.discontinue_product.discontinue_product_workflow import (
    DiscontinueProductWorkflow,
)
from api.workflows.products.publish_product.publish_product_workflow import (
    PublishProductWorkflow,
)
from common.application_environment import ApplicationEnvironment
from domain.entities.product import Product


class DependencyContainer:
    @classmethod
    async def initialize(cls) -> None:
        cls.initialize_application_settings()
        await cls.initialize_local_environment()

    @classmethod
    def initialize_application_settings(cls) -> None:
        cls.application_settings = ApplicationSettings()  # type: ignore[reportCallIssue]

    @classmethod
    @asynccontextmanager
    async def get_cosmosdb_client(
        cls,
    ) -> AsyncGenerator[CosmosClient]:
        application_settings = cls.get_application_settings()

        async with CosmosClient(
            application_settings.cosmos_db_no_sql_url,
            application_settings.cosmos_db_no_sql_key.get_secret_value(),
        ) as cosmosdb_client:
            yield cosmosdb_client

    @classmethod
    @asynccontextmanager
    async def get_cosmosdb_database(
        cls,
    ) -> AsyncGenerator[DatabaseProxy]:
        application_settings = cls.get_application_settings()

        async with cls.get_cosmosdb_client() as cosmosdb_client:
            cosmosdb_database = cosmosdb_client.get_database_client(
                application_settings.cosmos_db_no_sql_database
            )
            yield cosmosdb_database

    @classmethod
    async def initialize_local_environment(cls) -> None:
        if ApplicationEnvironment.get_current() != ApplicationEnvironment.LOCAL:
            return

        application_settings = cls.get_application_settings()

        async with cls.get_cosmosdb_client() as cosmosdb_client:
            await cosmosdb_client.create_database_if_not_exists(
                application_settings.cosmos_db_no_sql_database
            )

        async with cls.get_cosmosdb_database() as cosmosdb_database:
            await cosmosdb_database.create_container_if_not_exists(
                id=Product.__name__, partition_key=PartitionKey("/id")
            )

    @classmethod
    def get_application_settings(cls) -> ApplicationSettings:
        return cls.application_settings

    @classmethod
    @asynccontextmanager
    async def get_publish_product_workflow(
        cls,
    ) -> AsyncGenerator[PublishProductWorkflow]:
        async with cls.get_cosmosdb_database() as cosmosdb_database:
            yield PublishProductWorkflow(cosmosdb_database=cosmosdb_database)

    @classmethod
    @asynccontextmanager
    async def get_discontinue_product_workflow(
        cls,
    ) -> AsyncGenerator[DiscontinueProductWorkflow]:
        async with cls.get_cosmosdb_database() as cosmosdb_database:
            yield DiscontinueProductWorkflow(cosmosdb_database=cosmosdb_database)
