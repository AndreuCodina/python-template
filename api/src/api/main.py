from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import (  # type: ignore[reportMissingTypeStubs]
    FastAPIInstrumentor,
)

from api.dependency_container import DependencyContainer
from api.workflows.products import product_router
from common.application_environment import ApplicationEnvironment


def add_telemetry(app: FastAPI) -> None:
    FastAPIInstrumentor.instrument_app(app)  # type: ignore[reportUnknownMemberType]


DependencyContainer.initialize()
openapi_url = (
    "/openapi.json"
    if ApplicationEnvironment.get_current() != ApplicationEnvironment.PRODUCTION
    else None
)
app = FastAPI(title="Python monorepo", version="0.1.0", openapi_url=openapi_url)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(product_router.router)
