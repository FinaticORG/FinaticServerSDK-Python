"""Type definitions for Finatic SDK.

This file is regenerated on each run - do not edit directly.
"""

from typing import Any, Generic, TypeVar

from typing_extensions import TypedDict

# Generic type variable for response data
T = TypeVar("T")


class FinaticResponse(TypedDict, Generic[T]):
    """Public response envelope; runtime values remain ordinary dictionaries."""

    traceId: str | None
    data: T | None
    warnings: list[dict[str, Any]]
    errors: list[dict[str, Any]]


# The generic type parameter is for static typing and IntelliSense only.
# The public v1 envelope structure is:
# {
#   "traceId": str | None,
#   "data": T | None,
#   "warnings": list[dict],
#   "errors": list[dict],
# }
