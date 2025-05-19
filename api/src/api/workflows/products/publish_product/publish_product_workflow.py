from api.workflows.products.publish_product.publish_product_request import (
    PublishProductRequest,
)
from api.workflows.products.publish_product.publish_product_response import (
    PublishProductResponse,
)


class PublishProductWorkflow:
    async def execute(self, request: PublishProductRequest) -> PublishProductResponse:
        return PublishProductResponse(id=request.name)
