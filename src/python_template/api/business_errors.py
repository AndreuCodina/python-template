from http import HTTPStatus

from fastapi import HTTPException


class BusinessError(HTTPException):
    def __init__(
        self,
        status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY,
        detail: str | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)


class NotFoundError(BusinessError):
    def __init__(self) -> None:
        super().__init__(status_code=HTTPStatus.NOT_FOUND)


class ProductAlreadyDiscontinuedError(BusinessError):
    def __init__(self) -> None:
        super().__init__(detail="ProductAlreadyDiscontinued")
