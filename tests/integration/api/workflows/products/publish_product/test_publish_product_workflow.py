import pytest
from wirio.service_provider import ServiceProvider

from python_template.api.workflows.products.publish_product.publish_product_workflow import (
    PublishProductWorkflow,
)
from tests.test_utils.builders.api.workflows.products.publish_product.publish_product_request_builder import (
    PublishProductRequestBuilder,
)


class TestPublishProductWorkflow:
    @pytest.fixture(autouse=True)
    async def setup(self, service_provider: ServiceProvider) -> None:
        self.workflow = await service_provider.get_required_service(
            PublishProductWorkflow
        )

    async def test_publish_product(self) -> None:
        request = PublishProductRequestBuilder().build()

        await self.workflow.execute(request)
