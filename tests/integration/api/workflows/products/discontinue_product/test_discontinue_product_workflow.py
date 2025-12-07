import pytest

from python_template.api.dependency_container import DependencyContainer
from python_template.api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from python_template.api.workflows.products.discontinue_product.discontinue_product_workflow import (
    DiscontinueProductWorkflow,
)
from python_template.common.business_error import ProductAlreadyDiscontinuedError
from python_template.domain.entities.product import Product
from tests.test_utils.builders.domain.entities.product_builder import ProductBuilder


class TestDiscontinueProductWorkflow:
    @pytest.fixture
    async def workflow_fixture(self) -> DiscontinueProductWorkflow:
        return await DependencyContainer.get_discontinue_product_workflow()

    @pytest.fixture(autouse=True)
    def setup(self, workflow_fixture: DiscontinueProductWorkflow) -> None:
        self.workflow = workflow_fixture

    async def test_discontinue_product(self) -> None:
        cosmos_database = await DependencyContainer.get_cosmos_database()
        product_container = cosmos_database.get_container_client(Product.__name__)
        product = ProductBuilder().build()
        await product_container.create_item(product.model_dump())
        request = DiscontinueProductRequest(id=product.id)

        await self.workflow.execute(request)

    async def test_fail_when_discontinuing_discontinued_product(self) -> None:
        cosmos_database = await DependencyContainer.get_cosmos_database()
        product_container = cosmos_database.get_container_client(Product.__name__)
        product = ProductBuilder().discontinued().build()
        await product_container.create_item(product.model_dump())
        request = DiscontinueProductRequest(id=product.id)

        with pytest.raises(ProductAlreadyDiscontinuedError):
            await self.workflow.execute(request)
