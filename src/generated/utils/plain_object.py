"""
Plain object conversion utility (Phase 2C).

Generated - do not edit directly.

Converts Pydantic models and class instances to plain dicts for consistent SDK output.
"""

from typing import Any, Dict, List, Union


def convert_to_plain_object(data: Any) -> Any:
    """Convert data to plain objects/dicts, ensuring no class instances are returned.

    Handles lists, dicts, Pydantic models, and recursively converts nested structures.

    Args:
        data: Data to convert (can be any type)

    Returns:
        Plain dict/list/primitive (no class instances)

    Example:
        >>> result = convert_to_plain_object(some_pydantic_model)
        >>> # Returns plain dict instead of Pydantic model instance
    """
    if data is None:
        return None

    if isinstance(data, list):
        return [convert_to_plain_object(item) for item in data]

    if isinstance(data, dict):
        # Recursively convert nested dicts
        return {key: convert_to_plain_object(value) for key, value in data.items()}

    # Check if it's an Enum (has _value_ attribute or is instance of Enum)
    try:
        from enum import Enum

        if isinstance(data, Enum):
            # Return the enum's value (e.g., "active" instead of PublicConnectionStatusEnum.ACTIVE)
            return data.value
    except ImportError:
        pass

    # Check if it's a Pydantic model (has model_dump or dict method)
    if hasattr(data, "model_dump"):
        # Pydantic v2
        return convert_to_plain_object(data.model_dump())
    elif hasattr(data, "dict"):
        # Pydantic v1
        return convert_to_plain_object(data.dict())
    elif hasattr(data, "__dict__"):
        # Generic class instance - convert to dict
        return convert_to_plain_object(data.__dict__)

    # Primitive types (str, int, float, bool, etc.) - return as-is
    return data
