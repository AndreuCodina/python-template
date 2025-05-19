from decimal import Decimal

from pydantic import BaseModel


class PublishProductRequest(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
