from pydantic import BaseModel


class PublishProductResponse(BaseModel):
    id: str
