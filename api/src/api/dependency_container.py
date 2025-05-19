from azure.cosmos import CosmosClient, PartitionKey

from api.application_settings import ApplicationSettings
from api.workflows.products.publish_product.publish_product_workflow import (
    PublishProductWorkflow,
)
from common.application_environment import ApplicationEnvironment
from domain.entities.product import Product


class DependencyContainer:
    @classmethod
    def initialize(cls) -> None:
        cls.initialize_application_settings()
        cls.initialize_local_environment()

    @classmethod
    def initialize_application_settings(cls) -> None:
        cls.application_settings = ApplicationSettings()  # type: ignore[reportCallIssue]

    @classmethod
    def initialize_local_environment(cls) -> None:
        if ApplicationEnvironment.get_current() != ApplicationEnvironment.LOCAL:
            return

        with CosmosClient(
            cls.get_application_settings().cosmos_db_no_sql_url,
            cls.get_application_settings().cosmos_db_no_sql_key.get_secret_value(),
        ) as cosmosdb_client:
            cosmosdb_client.create_database_if_not_exists(
                id=cls.get_application_settings().cosmos_db_no_sql_database
            )
            cosmosdb_database = cosmosdb_client.get_database_client(
                cls.get_application_settings().cosmos_db_no_sql_database
            )
            cosmosdb_database.create_container_if_not_exists(
                id=Product.__name__, partition_key=PartitionKey("/id")
            )

    @classmethod
    def get_application_settings(cls) -> ApplicationSettings:
        return cls.application_settings

    @classmethod
    def get_publish_product_workflow(cls) -> PublishProductWorkflow:
        return PublishProductWorkflow(
            application_settings=cls.get_application_settings()
        )
