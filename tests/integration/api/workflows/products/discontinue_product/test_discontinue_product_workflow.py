import pytest
from test_utils.builders.domain.entities.product_builder import ProductBuilder

from python_archetype.api.dependency_container import DependencyContainer
from python_archetype.api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from python_archetype.api.workflows.products.discontinue_product.discontinue_product_workflow import (
    DiscontinueProductWorkflow,
)
from python_archetype.domain.entities.product import Product


@pytest.fixture
async def workflow() -> DiscontinueProductWorkflow:
    return await DependencyContainer.get_discontinue_product_workflow()


@pytest.mark.integration
class TestDiscontinueProductWorkflow:
    async def test_discontinue_product(
        self, workflow: DiscontinueProductWorkflow
    ) -> None:
        application_settings = DependencyContainer.get_application_settings()
        cosmos_client = await DependencyContainer.get_cosmos_client()
        cosmos_database = cosmos_client.get_database_client(
            application_settings.cosmos_db_no_sql_database
        )
        product = ProductBuilder().build()
        product_container = cosmos_database.get_container_client(Product.__name__)
        await product_container.create_item(product.model_dump())
        request = DiscontinueProductRequest(id=product.id)

        await workflow.execute(request)
