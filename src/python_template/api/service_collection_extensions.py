import logging
from logging import Logger

from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from wirio.service_collection import ServiceCollection

from python_template.api.application_settings import ApplicationSettings
from python_template.common.application_environment import ApplicationEnvironment


def add_observability(
    services: ServiceCollection, application_settings: ApplicationSettings
) -> None:
    logging.basicConfig(level=application_settings.logging_level)

    def inject_logging() -> Logger:
        return logging.getLogger(__name__)

    services.add_singleton(inject_logging)

    if ApplicationEnvironment.get_current() != ApplicationEnvironment.LOCAL:
        configure_azure_monitor(
            connection_string=application_settings.application_insights_connection_string,
            credential=DefaultAzureCredential(),
            enable_live_metrics=True,
        )


def add_sqlmodel(services: ServiceCollection) -> None:
    def inject_async_engine(application_settings: ApplicationSettings) -> AsyncEngine:
        return create_async_engine(application_settings.postgresql_connection_string)

    services.add_singleton(inject_async_engine)

    def inject_async_sessionmaker(
        async_engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            async_engine, class_=AsyncSession, expire_on_commit=False
        )

    services.add_singleton(inject_async_sessionmaker)

    def inject_async_session(
        async_sessionmaker: async_sessionmaker[AsyncSession],
    ) -> AsyncSession:
        return async_sessionmaker()

    services.add_transient(inject_async_session)
