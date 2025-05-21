import pytest
from azure.cosmos.aio import DatabaseProxy

from api.dependency_container import DependencyContainer
from api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from domain.entities.product import Product
from test_utils.builders.domain.entities.product_builder import ProductBuilder


@pytest.mark.integration
class TestDiscontinueProductWorkflow:
    async def test_discontinue_product(self, cosmosdb_database: DatabaseProxy) -> None:
        product = ProductBuilder().build()
        await cosmosdb_database.get_container_client(Product.__name__).create_item(
            product.model_dump()
        )
        request = DiscontinueProductRequest(id=product.id)
        workflow = DependencyContainer.get_discontinue_product_workflow()

        await workflow.execute(request)
