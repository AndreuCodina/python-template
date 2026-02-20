import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from wirio.service_provider import ServiceProvider

from python_template.api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from python_template.api.workflows.products.discontinue_product.discontinue_product_workflow import (
    DiscontinueProductWorkflow,
)
from python_template.common.business_errors import ProductAlreadyDiscontinuedError
from tests.test_utils.builders.domain.entities.product_builder import ProductBuilder


class TestDiscontinueProductWorkflow:
    @pytest.fixture(autouse=True)
    async def setup(self, service_provider: ServiceProvider) -> None:
        self.workflow = await service_provider.get_required_service(
            DiscontinueProductWorkflow
        )
        self.sql_session = await service_provider.get_required_service(AsyncSession)

    async def test_discontinue_product(self) -> None:
        product = ProductBuilder().build()
        self.sql_session.add(product)
        await self.sql_session.commit()
        request = DiscontinueProductRequest(id=product.id)

        await self.workflow.execute(request)

    async def test_fail_when_discontinue_discontinued_product(self) -> None:
        product = ProductBuilder().discontinued().build()
        self.sql_session.add(product)
        await self.sql_session.commit()
        request = DiscontinueProductRequest(id=product.id)

        with pytest.raises(ProductAlreadyDiscontinuedError):
            await self.workflow.execute(request)
