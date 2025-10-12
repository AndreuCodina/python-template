from decimal import Decimal

from python_template.domain.entities.product import Product


class TestProduct:
    def test_publish_product(self) -> None:
        Product(name="Product name", price=Decimal("1.0"), is_discontinued=False)
