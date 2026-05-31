import uuid
from decimal import Decimal
from uuid import UUID

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: UUID = Field(default_factory=uuid.uuid7, primary_key=True)
    name: str
    description: str | None = None
    price: Decimal
    is_discontinued: bool
    discontinuation_reason: str | None = None
