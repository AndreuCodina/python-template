from fastapi import APIRouter

from api.dependency_container import DependencyContainer
from api.workflows.products.publish_product.publish_product_request import (
    PublishProductRequest,
)
from api.workflows.products.publish_product.publish_product_response import (
    PublishProductResponse,
)

router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"],
)


@router.post("")
async def publish_product(request: PublishProductRequest) -> PublishProductResponse:
    return await DependencyContainer.get_publish_product_workflow().execute(request)
