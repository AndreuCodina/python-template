from azure.cosmos.aio import CosmosClient

from api.application_settings import ApplicationSettings
from api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from domain.entities.product import Product


class DiscontinueProductWorkflow:
    def __init__(self, application_settings: ApplicationSettings) -> None:
        self.application_settings = application_settings

    async def execute(self, request: DiscontinueProductRequest) -> None:
        async with CosmosClient(
            self.application_settings.cosmos_db_no_sql_url,
            self.application_settings.cosmos_db_no_sql_key.get_secret_value(),
        ) as cosmosdb_client:
            cosmosdb_database = cosmosdb_client.get_database_client(
                self.application_settings.cosmos_db_no_sql_database
            )
            product_container = cosmosdb_database.get_container_client(Product.__name__)
            product = await product_container.read_item(
                item=request.id, partition_key=request.id
            )
            product = Product.model_validate(product)
            product.discontinue(request.discontinuation_reason)
            await product_container.replace_item(product.id, product.model_dump())
