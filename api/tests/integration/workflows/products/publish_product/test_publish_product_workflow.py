import pytest

from api.dependency_container import DependencyContainer
from test_utils.builders.api.workflows.products.publish_product.publish_product_request_builder import (
    PublishProductRequestBuilder,
)


@pytest.mark.integration
class TestPublishProductWorkflow:
    async def test_publish_product(self) -> None:
        request = PublishProductRequestBuilder().build()

        async with DependencyContainer.get_publish_product_workflow() as workflow:
            await workflow.execute(request)
