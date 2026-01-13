import uuid
from decimal import Decimal
from uuid import UUID

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: UUID = Field(default_factory=uuid.uuid7, primary_key=True)
    name: str = Field(min_length=5, max_length=100)
    description: str | None = None
    price: Decimal = Field(gt=0.0, decimal_places=2)
    is_discontinued: bool
    discontinuation_reason: str | None = None
