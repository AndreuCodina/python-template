import pytest
from aspy_dependency_injection.service_provider import ServiceProvider
from azure.cosmos.aio import DatabaseProxy

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
    @pytest.fixture(autouse=True)
    async def setup(self, service_provider: ServiceProvider) -> None:
        self.workflow = await service_provider.get_required_service(
            DiscontinueProductWorkflow
        )
        cosmos_database = await service_provider.get_required_service(DatabaseProxy)
        self.product_container = cosmos_database.get_container_client(Product.__name__)

    async def test_discontinue_product(self) -> None:
        product = ProductBuilder().build()
        await self.product_container.create_item(product.model_dump())
        request = DiscontinueProductRequest(id=product.id)

        await self.workflow.execute(request)

    async def test_fail_when_discontinuing_discontinued_product(self) -> None:
        product = ProductBuilder().discontinued().build()
        await self.product_container.create_item(product.model_dump())
        request = DiscontinueProductRequest(id=product.id)

        with pytest.raises(ProductAlreadyDiscontinuedError):
            await self.workflow.execute(request)
