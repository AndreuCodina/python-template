import logging
from logging import Logger

from azure.cosmos import PartitionKey
from azure.cosmos.aio import CosmosClient, DatabaseProxy
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import (
    configure_azure_monitor,  # pyright: ignore[reportUnknownVariableType]
)

from python_template.api.application_settings import ApplicationSettings
from python_template.api.workflows.products.discontinue_product.discontinue_product_workflow import (
    DiscontinueProductWorkflow,
)
from python_template.api.workflows.products.publish_product.publish_product_workflow import (
    PublishProductWorkflow,
)
from python_template.common.application_environment import ApplicationEnvironment
from python_template.domain.entities.product import Product


class DependencyContainer:
    _logger: Logger | None
    _application_settings: ApplicationSettings | None
    _cosmos_client: CosmosClient | None

    @classmethod
    async def initialize(cls) -> None:
        cls._logger = None
        cls._application_settings = None
        cls._cosmos_client = None
        await cls.initialize_database()

    @classmethod
    async def uninitialize(cls) -> None:
        if cls._cosmos_client is not None:
            await cls._cosmos_client.close()

    @classmethod
    def get_logger(cls) -> Logger:
        if cls._logger is not None:
            return cls._logger

        application_settings = cls.get_application_settings()
        logging.basicConfig(level=application_settings.logging_level)
        logger = logging.getLogger(__name__)
        cls._logger = logger

        if ApplicationEnvironment.get_current() != ApplicationEnvironment.LOCAL:
            configure_azure_monitor(
                connection_string=application_settings.application_insights_connection_string,
                credential=DefaultAzureCredential(),
                enable_live_metrics=True,
            )

        return cls._logger

    @classmethod
    def get_application_settings(cls) -> ApplicationSettings:
        if cls._application_settings is not None:
            return cls._application_settings

        cls._application_settings = ApplicationSettings()  # type: ignore[reportCallIssue]
        return cls._application_settings

    @classmethod
    async def get_cosmos_client(cls) -> CosmosClient:
        if cls._cosmos_client is not None:
            return cls._cosmos_client

        application_settings = cls.get_application_settings()
        cls._cosmos_client = await CosmosClient(
            application_settings.cosmos_db_no_sql_url,
            application_settings.cosmos_db_no_sql_key.get_secret_value(),
        ).__aenter__()
        return cls._cosmos_client

    @classmethod
    async def get_cosmos_database(cls) -> DatabaseProxy:
        application_settings = cls.get_application_settings()
        cosmos_client = await cls.get_cosmos_client()
        return cosmos_client.get_database_client(
            application_settings.cosmos_db_no_sql_database
        )

    @classmethod
    async def initialize_database(cls) -> None:
        if ApplicationEnvironment.get_current() != ApplicationEnvironment.LOCAL:
            return

        application_settings = cls.get_application_settings()
        cosmos_client = await cls.get_cosmos_client()
        await cosmos_client.create_database_if_not_exists(
            application_settings.cosmos_db_no_sql_database
        )
        cosmos_database = await cls.get_cosmos_database()
        await cosmos_database.create_container_if_not_exists(
            id=Product.__name__, partition_key=PartitionKey("/id")
        )

    @classmethod
    async def get_publish_product_workflow(
        cls,
    ) -> PublishProductWorkflow:
        return PublishProductWorkflow(cosmos_database=await cls.get_cosmos_database())

    @classmethod
    async def get_discontinue_product_workflow(
        cls,
    ) -> DiscontinueProductWorkflow:
        return DiscontinueProductWorkflow(
            cosmos_database=await cls.get_cosmos_database(),
            logger=cls.get_logger(),
        )
