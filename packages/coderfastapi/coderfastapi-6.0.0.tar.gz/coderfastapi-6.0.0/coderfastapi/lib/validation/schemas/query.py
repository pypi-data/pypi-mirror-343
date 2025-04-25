from typing import ClassVar, TypeVar

from codercore.lib.collection import Direction
from pydantic import BaseModel, field_validator

from coderfastapi.lib.validation.schemas.pagination import DeserializableCursor

MAX_LIMIT = 100
DEFAULT_LIMIT = 25
DEFAULT_ORDER_BY = "id"
ORDERABLE_PROPERTIES = (DEFAULT_ORDER_BY,)

T = TypeVar("T", str, tuple[str, ...])


class QueryParameters(BaseModel):
    __canonical_name__ = "QueryParameters"
    _max_limit: ClassVar[int] = MAX_LIMIT

    cursor: DeserializableCursor | None = None
    limit: int = DEFAULT_LIMIT

    @field_validator("limit")
    @classmethod
    def limit_within_bounds(cls, v: int) -> int:
        if v < 1 or v > cls._max_limit:
            raise ValueError(f"ensure limit is >= 1 and <= {cls._max_limit}")
        return v


class OrderableQueryParameters(QueryParameters):
    _orderable_properties: ClassVar[tuple[str]] = ORDERABLE_PROPERTIES

    order_by: str | tuple[str, ...] = DEFAULT_ORDER_BY
    order_direction: Direction = Direction.DESC

    @field_validator("order_by")
    @classmethod
    def validate_order_by(cls, v: T) -> T:
        if isinstance(v, str):
            order_by_values = (v,)
        else:
            order_by_values = v
        for value in order_by_values:
            if value not in cls._orderable_properties:
                raise ValueError(f"order_by must be one of {cls._orderable_properties}")
        return v
