from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from fastapi import FastAPI
from wirio import ServiceCollection

from python_template.api.application_settings import ApplicationSettings
from python_template.api.service_collection_extensions import (
    add_logging,
)
from python_template.api.services.email_service import EmailService
from python_template.api.workflows.products.discontinue_product.discontinue_product_workflow import (
    DiscontinueProductWorkflow,
)
from python_template.api.workflows.products.product_router import product_router
from python_template.api.workflows.products.publish_product.publish_product_workflow import (
    PublishProductWorkflow,
)

app = FastAPI()
app.include_router(product_router)

services = ServiceCollection()
services.configure_fastapi(app)

if not services.environment.is_local:
    services.configuration.add_azure_key_vault(services.configuration["key_vault_url"])

application_settings = services.configuration[ApplicationSettings]
add_logging(services, application_settings.logging_level)

if not services.environment.is_local:
    configure_azure_monitor(
        connection_string=application_settings.application_insights_connection_string,
        credential=DefaultAzureCredential(),
        enable_live_metrics=True,
    )

services.add_sqlmodel(application_settings.postgresql_connection_string)
services.add_transient(EmailService)
services.add_transient(PublishProductWorkflow)
services.add_transient(DiscontinueProductWorkflow)
