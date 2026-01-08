from azure.cosmos.aio import DatabaseProxy

from python_template.api.services.email_service import EmailService
from python_template.api.workflows.products.publish_product.publish_product_request import (
    PublishProductRequest,
)
from python_template.api.workflows.products.publish_product.publish_product_response import (
    PublishProductResponse,
)
from python_template.domain.entities.product import Product


class PublishProductWorkflow:
    def __init__(
        self, cosmos_database: DatabaseProxy, email_service: EmailService
    ) -> None:
        self.product_container = cosmos_database.get_container_client(Product.__name__)
        self.email_service = email_service

    async def execute(self, request: PublishProductRequest) -> PublishProductResponse:
        product = Product(
            name=request.name,
            description=request.description,
            price=request.price,
            is_discontinued=False,
        )
        await self.product_container.create_item(product.model_dump())
        await self.email_service.send_email()
        return PublishProductResponse(id=product.id)
