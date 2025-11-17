import pytest

from python_template.api.dependency_container import DependencyContainer
from python_template.api.workflows.products.publish_product.publish_product_workflow import (
    PublishProductWorkflow,
)
from tests.test_utils.builders.api.workflows.products.publish_product.publish_product_request_builder import (
    PublishProductRequestBuilder,
)


class TestPublishProductWorkflow:
    @pytest.fixture
    async def workflow_fixture(self) -> PublishProductWorkflow:
        return await DependencyContainer.get_publish_product_workflow()

    @pytest.fixture(autouse=True)
    def setup(self, workflow_fixture: PublishProductWorkflow) -> None:
        self.workflow = workflow_fixture

    async def test_publish_product(self) -> None:
        request = PublishProductRequestBuilder().build()

        await self.workflow.execute(request)
