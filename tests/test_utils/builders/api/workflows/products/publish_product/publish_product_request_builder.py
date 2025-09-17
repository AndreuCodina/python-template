from decimal import Decimal

from python_seed.api.workflows.products.publish_product.publish_product_request import (
    PublishProductRequest,
)


class PublishProductRequestBuilder:
    def build(self) -> PublishProductRequest:
        return PublishProductRequest(
            name="Table",
            description="Description",
            price=Decimal("10.0"),
        )
