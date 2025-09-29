from decimal import Decimal

from pydantic import Field

from python_template.domain.entity import Entity


class Product(Entity):
    name: str = Field(min_length=5, max_length=100)
    description: str | None = None
    price: Decimal = Field(gt=Decimal("0.0"))
    is_discontinued: bool
    discontinuation_reason: str | None = None
