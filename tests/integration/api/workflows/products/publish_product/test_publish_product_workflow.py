import pytest
from wirio.service_container import ServiceContainer

from python_template.api.workflows.products.publish_product.publish_product_workflow import (
    PublishProductWorkflow,
)
from tests.test_utils.builders.api.workflows.products.publish_product.publish_product_request_builder import (
    PublishProductRequestBuilder,
)


class TestPublishProductWorkflow:
    @pytest.fixture(autouse=True)
    async def setup(self, services_fixture: ServiceContainer) -> None:
        self.workflow = await services_fixture.get(PublishProductWorkflow)

    async def test_publish_product(self) -> None:
        request = PublishProductRequestBuilder().build()

        await self.workflow.execute(request)
