from fastapi import APIRouter

from python_archetype.api.dependency_container import DependencyContainer
from python_archetype.api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from python_archetype.api.workflows.products.publish_product.publish_product_request import (
    PublishProductRequest,
)
from python_archetype.api.workflows.products.publish_product.publish_product_response import (
    PublishProductResponse,
)

router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"],
)


@router.post("")
async def publish_product(request: PublishProductRequest) -> PublishProductResponse:
    async with DependencyContainer.get_publish_product_workflow() as workflow:
        return await workflow.execute(request)


@router.post("/discontinue")
async def discontinue_product(request: DiscontinueProductRequest) -> None:
    async with DependencyContainer.get_discontinue_product_workflow() as workflow:
        return await workflow.execute(request)
