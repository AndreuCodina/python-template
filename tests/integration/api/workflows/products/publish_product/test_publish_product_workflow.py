import pytest

from python_template.api.dependency_container import DependencyContainer
from python_template.api.workflows.products.publish_product.publish_product_workflow import (
    PublishProductWorkflow,
)
from tests.test_utils.builders.api.workflows.products.publish_product.publish_product_request_builder import (
    PublishProductRequestBuilder,
)


@pytest.fixture
async def workflow() -> PublishProductWorkflow:
    return await DependencyContainer.get_publish_product_workflow()


class TestPublishProductWorkflow:
    async def test_publish_product(self, workflow: PublishProductWorkflow) -> None:
        request = PublishProductRequestBuilder().build()

        await workflow.execute(request)
