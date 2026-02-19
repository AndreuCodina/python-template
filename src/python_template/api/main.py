from fastapi import FastAPI
from wirio.service_collection import ServiceCollection

from python_template.api.application_settings import ApplicationSettings
from python_template.api.service_collection_extensions import (
    add_azure_monitor,
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
application_settings = ApplicationSettings()  # ty:ignore[missing-argument]
services.add_singleton(ApplicationSettings, application_settings)
add_logging(services, application_settings.logging_level)
add_azure_monitor(application_settings.application_insights_connection_string)
services.add_sqlmodel(application_settings.postgresql_connection_string)
services.add_transient(EmailService)
services.add_transient(PublishProductWorkflow)
services.add_transient(DiscontinueProductWorkflow)
services.configure_fastapi(app)
