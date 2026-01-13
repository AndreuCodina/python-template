from uuid import UUID

from pydantic import BaseModel


class PublishProductResponse(BaseModel):
    id: UUID
