from http import HTTPStatus
from logging import Logger

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from python_template.api.workflows.products.discontinue_product.discontinue_product_request import (
    DiscontinueProductRequest,
)
from python_template.common.business_errors import (
    BusinessError,
    ProductAlreadyDiscontinuedError,
)
from python_template.domain.entities import Product


class DiscontinueProductWorkflow:
    def __init__(self, sql_session: AsyncSession, logger: Logger) -> None:
        self.sql_session = sql_session
        self.logger = logger

    async def execute(self, request: DiscontinueProductRequest) -> None:
        product = (
            (
                await self.sql_session.execute(
                    select(Product).where(Product.id == request.id)
                )
            )
            .unique()
            .scalar_one_or_none()
        )

        if product is None:
            raise BusinessError(status_code=HTTPStatus.NOT_FOUND)

        if product.is_discontinued:
            self.logger.warning(
                "Product {product_id} is already discontinued",
                extra={"product_id": product.id},
            )
            raise ProductAlreadyDiscontinuedError

        product.is_discontinued = True
        product.discontinuation_reason = request.discontinuation_reason
        self.sql_session.add(product)
        await self.sql_session.commit()
