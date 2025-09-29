from azure.cosmos.aio import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError

from python_template.api.application_settings import ApplicationSettings
from python_template.api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from python_template.common.business_error import EntityNotFoundError
from python_template.domain.entities.product import Product


class DiscontinueProductWorkflow:
    def __init__(
        self, cosmos_client: CosmosClient, application_settings: ApplicationSettings
    ) -> None:
        cosmos_database = cosmos_client.get_database_client(
            application_settings.cosmos_db_no_sql_database
        )
        self.product_container = cosmos_database.get_container_client(Product.__name__)

    async def execute(self, request: DiscontinueProductRequest) -> None:
        product = await self.get_product(request.id)
        product.discontinue(request.discontinuation_reason)
        await self.product_container.replace_item(product.id, product.model_dump())

    async def get_product(self, product_id: str) -> Product:
        try:
            return Product.model_validate(
                await self.product_container.read_item(
                    item=product_id, partition_key=product_id
                )
            )
        except CosmosResourceNotFoundError:
            raise EntityNotFoundError from None
