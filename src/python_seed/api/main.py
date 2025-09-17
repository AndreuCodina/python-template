from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from python_seed.api.dependency_container import DependencyContainer
from python_seed.api.workflows.products import product_router
from python_seed.common.application_environment import ApplicationEnvironment


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    await DependencyContainer.initialize()
    yield
    await DependencyContainer.uninitialize()


openapi_url = (
    "/openapi.json"
    if ApplicationEnvironment.get_current() != ApplicationEnvironment.PRODUCTION
    else None
)
app = FastAPI(
    openapi_url=openapi_url,
    lifespan=lifespan,
)
app.include_router(product_router.router)
