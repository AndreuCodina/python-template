import logging
from logging import Logger

from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from wirio.service_collection import ServiceCollection

from python_template.common.application_environment import ApplicationEnvironment


def add_logging(services: ServiceCollection, logging_level: str) -> None:
    logging.basicConfig(level=logging_level)
    services.add_singleton(Logger, logging.getLogger(__name__))


def add_azure_monitor(application_insights_connection_string: str) -> None:
    if ApplicationEnvironment.get_current() != ApplicationEnvironment.LOCAL:
        configure_azure_monitor(
            connection_string=application_insights_connection_string,
            credential=DefaultAzureCredential(),
            enable_live_metrics=True,
        )
