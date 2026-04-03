from datetime import datetime, timezone
from typing import Annotated, Any, Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.functional_serializers import PlainSerializer

UTCDatetime = Annotated[
    datetime,
    PlainSerializer(
        lambda v: (v.replace(tzinfo=timezone.utc) if v.tzinfo is None else v)
        .isoformat()
        .replace("+00:00", "Z"),
        return_type=str,
        when_used="json",
    ),
]

T = TypeVar("T")


class DataResponse(BaseModel, Generic[T]):
    data: T


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    page: int
    size: int
    has_next: bool
