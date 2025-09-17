from azure.cosmos.aio import CosmosClient

from python_seed.api.application_settings import ApplicationSettings
from python_seed.api.workflows.products.publish_product.publish_product_request import (
    PublishProductRequest,
)
from python_seed.api.workflows.products.publish_product.publish_product_response import (
    PublishProductResponse,
)
from python_seed.domain.entities.product import Product


class PublishProductWorkflow:
    def __init__(
        self, cosmos_client: CosmosClient, application_settings: ApplicationSettings
    ) -> None:
        self.cosmos_client = cosmos_client
        self.application_settings = application_settings

    async def execute(self, request: PublishProductRequest) -> PublishProductResponse:
        cosmos_database = self.cosmos_client.get_database_client(
            self.application_settings.cosmos_db_no_sql_database
        )
        product_container = cosmos_database.get_container_client(Product.__name__)
        product = Product.publish(
            name=request.name,
            description=request.description,
            price=request.price,
        )
        await product_container.create_item(product.model_dump())
        return PublishProductResponse(id=product.id)
