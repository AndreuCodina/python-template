from azure.cosmos.aio import DatabaseProxy

from python_archetype.api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from python_archetype.domain.entities.product import Product


class DiscontinueProductWorkflow:
    def __init__(self, cosmosdb_database: DatabaseProxy) -> None:
        self.cosmosdb_database = cosmosdb_database

    async def execute(self, request: DiscontinueProductRequest) -> None:
        product_container = self.cosmosdb_database.get_container_client(
            Product.__name__
        )
        product_dict = await product_container.read_item(
            item=request.id, partition_key=request.id
        )
        product = Product.model_validate(product_dict)
        product.discontinue(request.discontinuation_reason)
        await product_container.replace_item(product.id, product.model_dump())
