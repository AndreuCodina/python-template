from typing import Annotated

from fastapi import APIRouter
from wirio.annotations import FromServices

from python_template.api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from python_template.api.workflows.products.discontinue_product.discontinue_product_workflow import (
    DiscontinueProductWorkflow,
)
from python_template.api.workflows.products.publish_product.publish_product_request import (
    PublishProductRequest,
)
from python_template.api.workflows.products.publish_product.publish_product_response import (
    PublishProductResponse,
)
from python_template.api.workflows.products.publish_product.publish_product_workflow import (
    PublishProductWorkflow,
)

product_router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"],
)


@product_router.post("")
async def publish_product(
    request: PublishProductRequest,
    workflow: Annotated[PublishProductWorkflow, FromServices()],
) -> PublishProductResponse:
    return await workflow.execute(request)


@product_router.post("/discontinue")
async def discontinue_product(
    request: DiscontinueProductRequest,
    workflow: Annotated[DiscontinueProductWorkflow, FromServices()],
) -> None:
    await workflow.execute(request)
