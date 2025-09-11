from azure.cosmos.aio import DatabaseProxy

from python_archetype.api.workflows.products.publish_product.publish_product_request import (
    PublishProductRequest,
)
from python_archetype.api.workflows.products.publish_product.publish_product_response import (
    PublishProductResponse,
)
from python_archetype.domain.entities.product import Product


class PublishProductWorkflow:
    def __init__(self, cosmosdb_database: DatabaseProxy) -> None:
        self.cosmosdb_database = cosmosdb_database

    async def execute(self, request: PublishProductRequest) -> PublishProductResponse:
        product_container = self.cosmosdb_database.get_container_client(
            Product.__name__
        )
        product = Product.publish(
            name=request.name,
            description=request.description,
            price=request.price,
        )
        await product_container.create_item(product.model_dump())
        return PublishProductResponse(id=product.id)
