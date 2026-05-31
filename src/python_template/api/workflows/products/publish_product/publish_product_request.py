from decimal import Decimal

from pydantic import BaseModel, Field


class PublishProductRequest(BaseModel):
    name: str = Field(min_length=5, max_length=100)
    description: str | None = None
    price: Decimal = Field(gt=0.0, decimal_places=2)
