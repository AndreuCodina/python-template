import pytest

from common.business_error import BusinessError
from test_utils.builders.domain.entities.product_builder import ProductBuilder


@pytest.mark.unit
class TestProduct:
    def test_discontinue_product(self) -> None:
        product = ProductBuilder().build()

        product.discontinue()

    def test_fail_when_discontinuing_discontinued_product(self) -> None:
        product = ProductBuilder().discontinued().build()

        with pytest.raises(BusinessError):
            product.discontinue()
