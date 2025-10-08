import datetime
import uuid
from collections.abc import Callable
from typing import Any, Literal, override

from pydantic import BaseModel, Field
from pydantic.main import IncEx


class Entity(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    create_date: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.UTC)
    )

    @override
    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "json",  # noqa: PYI051
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_computed_fields: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        fallback: Callable[[Any], Any] | None = None,
        serialize_as_any: bool = False,
    ) -> dict[str, Any]:
        return super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
        )
