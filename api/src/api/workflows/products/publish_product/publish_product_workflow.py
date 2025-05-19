from azure.cosmos.aio import CosmosClient

from api.application_settings import ApplicationSettings
from api.workflows.products.publish_product.publish_product_request import (
    PublishProductRequest,
)
from api.workflows.products.publish_product.publish_product_response import (
    PublishProductResponse,
)
from domain.entities.product import Product


class PublishProductWorkflow:
    def __init__(self, application_settings: ApplicationSettings) -> None:
        self.application_settings = application_settings

    async def execute(self, request: PublishProductRequest) -> PublishProductResponse:
        async with CosmosClient(
            self.application_settings.cosmos_db_no_sql_url,
            self.application_settings.cosmos_db_no_sql_key.get_secret_value(),
        ) as cosmosdb_client:
            cosmosdb_database = cosmosdb_client.get_database_client(
                self.application_settings.cosmos_db_no_sql_database
            )
            product_container = cosmosdb_database.get_container_client(Product.__name__)
            product = Product.publish(
                name=request.name,
                description=request.description,
                price=request.price,
            )
            await product_container.create_item(product.model_dump())
            return PublishProductResponse(id=product.id)
