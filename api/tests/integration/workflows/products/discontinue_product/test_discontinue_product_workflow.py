import pytest

from api.dependency_container import DependencyContainer
from api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from domain.entities.product import Product
from test_utils.builders.domain.entities.product_builder import ProductBuilder


@pytest.mark.integration
class TestDiscontinueProductWorkflow:
    async def test_discontinue_product(self) -> None:
        async with DependencyContainer.get_cosmosdb_database() as cosmosdb_database:
            product = ProductBuilder().build()
            await cosmosdb_database.get_container_client(Product.__name__).create_item(
                product.model_dump()
            )
            request = DiscontinueProductRequest(id=product.id)

            async with (
                DependencyContainer.get_discontinue_product_workflow() as workflow
            ):
                await workflow.execute(request)
