from sqlmodel.ext.asyncio.session import AsyncSession

from python_template.api.services.email_service import EmailService
from python_template.api.workflows.products.publish_product.publish_product_request import (
    PublishProductRequest,
)
from python_template.api.workflows.products.publish_product.publish_product_response import (
    PublishProductResponse,
)
from python_template.domain.entities import Product


class PublishProductWorkflow:
    def __init__(self, sql_session: AsyncSession, email_service: EmailService) -> None:
        self.sql_session = sql_session
        self.email_service = email_service

    async def execute(self, request: PublishProductRequest) -> PublishProductResponse:
        product = Product(
            name=request.name,
            description=request.description,
            price=request.price,
            is_discontinued=False,
        )
        self.sql_session.add(product)
        await self.sql_session.commit()
        await self.email_service.send_email()
        return PublishProductResponse(id=product.id)
