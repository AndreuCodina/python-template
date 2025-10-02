from http import HTTPStatus
from logging import Logger

from azure.cosmos.aio import DatabaseProxy
from azure.cosmos.exceptions import CosmosResourceNotFoundError

from python_template.api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from python_template.common.business_error import (
    BusinessError,
    ProductAlreadyDiscontinuedError,
)
from python_template.domain.entities.product import Product


class DiscontinueProductWorkflow:
    def __init__(self, cosmos_database: DatabaseProxy, logger: Logger) -> None:
        self.product_container = cosmos_database.get_container_client(Product.__name__)
        self.logger = logger

    async def execute(self, request: DiscontinueProductRequest) -> None:
        product = await self.get_product(request.id)

        if product.is_discontinued:
            self.logger.warning(
                "Product {product_id} is already discontinued",
                extra={"product_id": product.id},
            )
            raise ProductAlreadyDiscontinuedError

        product.is_discontinued = True
        product.discontinuation_reason = request.discontinuation_reason
        await self.product_container.replace_item(product.id, product.model_dump())

    async def get_product(self, product_id: str) -> Product:
        try:
            return Product.model_validate(
                await self.product_container.read_item(
                    item=product_id, partition_key=product_id
                )
            )
        except CosmosResourceNotFoundError:
            raise BusinessError(status_code=HTTPStatus.NOT_FOUND) from None
