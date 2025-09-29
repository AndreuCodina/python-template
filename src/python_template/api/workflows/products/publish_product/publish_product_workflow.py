from azure.cosmos.aio import CosmosClient

from python_template.api.application_settings import ApplicationSettings
from python_template.api.workflows.products.publish_product.publish_product_request import (
    PublishProductRequest,
)
from python_template.api.workflows.products.publish_product.publish_product_response import (
    PublishProductResponse,
)
from python_template.domain.entities.product import Product


class PublishProductWorkflow:
    def __init__(
        self, cosmos_client: CosmosClient, application_settings: ApplicationSettings
    ) -> None:
        cosmos_database = cosmos_client.get_database_client(
            application_settings.cosmos_db_no_sql_database
        )
        self.product_container = cosmos_database.get_container_client(Product.__name__)

    async def execute(self, request: PublishProductRequest) -> PublishProductResponse:
        product = Product.publish(
            name=request.name,
            description=request.description,
            price=request.price,
        )
        await self.product_container.create_item(product.model_dump())
        return PublishProductResponse(id=product.id)
