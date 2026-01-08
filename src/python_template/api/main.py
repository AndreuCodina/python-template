import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import Logger

from aspy_dependency_injection.service_collection import ServiceCollection
from azure.cosmos import PartitionKey
from azure.cosmos.aio import CosmosClient, DatabaseProxy
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import (
    configure_azure_monitor,  # pyright: ignore[reportUnknownVariableType]
)
from fastapi import FastAPI

from python_template.api.application_settings import ApplicationSettings
from python_template.api.services.email_service import EmailService
from python_template.api.workflows.products.discontinue_product.discontinue_product_workflow import (
    DiscontinueProductWorkflow,
)
from python_template.api.workflows.products.product_router import product_router
from python_template.api.workflows.products.publish_product.publish_product_workflow import (
    PublishProductWorkflow,
)
from python_template.common.application_environment import ApplicationEnvironment
from python_template.domain.entities.product import Product


def inject_application_settings() -> ApplicationSettings:
    return ApplicationSettings()  # ty:ignore[missing-argument]


def inject_logging() -> Logger:
    return logging.getLogger(__name__)


def inject_cosmos_client(
    application_settings: ApplicationSettings,
) -> CosmosClient:
    return CosmosClient(
        url=application_settings.cosmos_db_no_sql_url,
        credential=application_settings.cosmos_db_no_sql_key.get_secret_value(),
    )


def inject_cosmos_database(
    application_settings: ApplicationSettings, cosmos_client: CosmosClient
) -> DatabaseProxy:
    return cosmos_client.get_database_client(
        application_settings.cosmos_db_no_sql_database
    )


def configure_services() -> ServiceCollection:
    services = ServiceCollection()
    services.add_singleton(inject_application_settings)
    services.add_singleton(inject_logging)
    services.add_singleton(inject_cosmos_client)
    services.add_transient(inject_cosmos_database)
    services.add_transient(EmailService)
    services.add_transient(PublishProductWorkflow)
    services.add_transient(DiscontinueProductWorkflow)
    return services


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
        async with configure_services().build_service_provider() as service_provider:
            application_settings = await service_provider.get_required_service(
                ApplicationSettings
            )
            logging.basicConfig(level=application_settings.logging_level)

            if ApplicationEnvironment.get_current() != ApplicationEnvironment.LOCAL:
                configure_azure_monitor(
                    connection_string=application_settings.application_insights_connection_string,
                    credential=DefaultAzureCredential(),
                    enable_live_metrics=True,
                )

            if ApplicationEnvironment.get_current() == ApplicationEnvironment.LOCAL:
                cosmos_client = await service_provider.get_required_service(
                    CosmosClient
                )
                await cosmos_client.create_database_if_not_exists(
                    application_settings.cosmos_db_no_sql_database
                )
                cosmos_database = await service_provider.get_required_service(
                    DatabaseProxy
                )
                await cosmos_database.create_container_if_not_exists(
                    id=Product.__name__, partition_key=PartitionKey("/id")
                )
        yield

    openapi_url = (
        "/openapi.json"
        if ApplicationEnvironment.get_current() != ApplicationEnvironment.PRODUCTION
        else None
    )
    app = FastAPI(openapi_url=openapi_url, lifespan=lifespan)
    app.include_router(product_router)
    return app


app = create_app()
services = configure_services()
services.configure_fastapi(app)
