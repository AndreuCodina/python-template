from decimal import Decimal
from typing import Self

from python_template.domain.entities import Product


class ProductBuilder:
    def __init__(self) -> None:
        self.is_discontinued = False

    def build(self) -> Product:
        return Product(
            name="Table",
            description="Description",
            price=Decimal("10.0"),
            is_discontinued=self.is_discontinued,
        )

    def discontinued(self) -> Self:
        self.is_discontinued = True
        return self
