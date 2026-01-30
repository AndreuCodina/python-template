from fastapi import FastAPI
from wirio.service_collection import ServiceCollection

from python_template.api.application_settings import ApplicationSettings
from python_template.api.service_collection_extensions import (
    add_observability,
    add_sqlmodel,
)
from python_template.api.services.email_service import EmailService
from python_template.api.workflows.products.discontinue_product.discontinue_product_workflow import (
    DiscontinueProductWorkflow,
)
from python_template.api.workflows.products.product_router import product_router
from python_template.api.workflows.products.publish_product.publish_product_workflow import (
    PublishProductWorkflow,
)
from python_template.common.application_environment import ApplicationEnvironment

openapi_url = (
    "/openapi.json"
    if ApplicationEnvironment.get_current() != ApplicationEnvironment.PRODUCTION
    else None
)
app = FastAPI(openapi_url=openapi_url)
app.include_router(product_router)

services = ServiceCollection()
application_settings = ApplicationSettings()  # ty:ignore[missing-argument]
services.add_singleton(ApplicationSettings, application_settings)
add_observability(services, application_settings)
add_sqlmodel(services)
services.add_transient(EmailService)
services.add_transient(PublishProductWorkflow)
services.add_transient(DiscontinueProductWorkflow)
services.configure_fastapi(app)
