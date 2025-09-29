from http import HTTPStatus

from fastapi import HTTPException


class BusinessError(HTTPException):
    def __init__(
        self,
        detail: str | None = None,
        status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail
            if detail is not None
            else self.__class__.__name__.removesuffix("Error"),
        )


class EntityNotFoundError(BusinessError):
    def __init__(self) -> None:
        super().__init__(status_code=HTTPStatus.NOT_FOUND)


class ProductAlreadyDiscontinuedError(BusinessError):
    pass
