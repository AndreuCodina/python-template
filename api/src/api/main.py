from fastapi import FastAPI

from api.dependency_container import DependencyContainer
from api.workflows.products import product_router

DependencyContainer.initialize()
app = FastAPI()
app.include_router(product_router.router)


@app.get("/")
async def root() -> str:
    return "Hello"
