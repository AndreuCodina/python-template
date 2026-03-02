import logging
from logging import Logger

from wirio.service_collection import ServiceCollection


def add_logging(services: ServiceCollection, logging_level: str) -> None:
    logging.basicConfig(level=logging_level)
    services.add_singleton(Logger, logging.getLogger(__name__))
