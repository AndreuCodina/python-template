from typing import Optional

from sqlmodel import (
    Field,  # type: ignore
    SQLModel,
)


class Product(SQLModel, table=True):
    __tablename__ = "product"  # type: ignore

    id: int = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    is_discontinued: bool
