from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import (  # type: ignore[reportMissingTypeStubs]
    FastAPIInstrumentor,
)

from python_archetype.api.dependency_container import DependencyContainer
from python_archetype.api.workflows.products import product_router
from python_archetype.common.application_environment import ApplicationEnvironment


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    await DependencyContainer.initialize()
    yield


def add_telemetry(app: FastAPI) -> None:
    FastAPIInstrumentor.instrument_app(app)  # type: ignore[reportUnknownMemberType]


openapi_url = (
    "/openapi.json"
    if ApplicationEnvironment.get_current() != ApplicationEnvironment.PRODUCTION
    else None
)
app = FastAPI(
    title="Python monorepo",
    version="0.1.0",
    openapi_url=openapi_url,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(product_router.router)
