from fastapi import FastAPI

from api.dependency_container import DependencyContainer
from api.workflows.products import product_router
from common.application_environment import ApplicationEnvironment

DependencyContainer.initialize()
openapi_url = (
    "/openapi.json"
    if ApplicationEnvironment.get_current() != ApplicationEnvironment.PRODUCTION
    else None
)
app = FastAPI(title="Python monorepo", version="0.1.0", openapi_url=openapi_url)
app.include_router(product_router.router)
