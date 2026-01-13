from uuid import UUID

from pydantic import BaseModel


class DiscontinueProductRequest(BaseModel):
    id: UUID
    discontinuation_reason: str | None = None
