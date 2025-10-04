from fastapi import APIRouter

from python_template.api.dependency_container import DependencyContainer
from python_template.api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from python_template.api.workflows.products.publish_product.publish_product_request import (
    PublishProductRequest,
)
from python_template.api.workflows.products.publish_product.publish_product_response import (
    PublishProductResponse,
)

product_router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"],
)


@product_router.post("")
async def publish_product(request: PublishProductRequest) -> PublishProductResponse:
    workflow = await DependencyContainer.get_publish_product_workflow()
    return await workflow.execute(request)


@product_router.post("/discontinue")
async def discontinue_product(request: DiscontinueProductRequest) -> None:
    workflow = await DependencyContainer.get_discontinue_product_workflow()
    await workflow.execute(request)
