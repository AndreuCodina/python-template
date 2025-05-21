from pydantic import BaseModel


class DiscontinueProductRequest(BaseModel):
    id: str
    discontinuation_reason: str | None = None
