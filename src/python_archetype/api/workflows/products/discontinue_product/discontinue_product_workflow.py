from azure.cosmos.aio import CosmosClient

from python_archetype.api.application_settings import ApplicationSettings
from python_archetype.api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from python_archetype.domain.entities.product import Product


class DiscontinueProductWorkflow:
    def __init__(
        self, cosmos_client: CosmosClient, application_settings: ApplicationSettings
    ) -> None:
        self.cosmos_client = cosmos_client
        self.application_settings = application_settings

    async def execute(self, request: DiscontinueProductRequest) -> None:
        cosmos_database = self.cosmos_client.get_database_client(
            self.application_settings.cosmos_db_no_sql_database
        )
        product_container = cosmos_database.get_container_client(Product.__name__)
        product_dict = await product_container.read_item(
            item=request.id, partition_key=request.id
        )
        product = Product.model_validate(product_dict)
        product.discontinue(request.discontinuation_reason)
        await product_container.replace_item(product.id, product.model_dump())
