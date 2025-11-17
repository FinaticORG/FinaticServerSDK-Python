"""
Generated utility functions (Phase 2B).

This file is regenerated on each run - do not edit directly.
"""

from .cache import generate_cache_key, get_cache
from .enum_coercion import coerce_enum_value
from .error_handling import ApiError, FinaticError, ValidationError, handle_error
from .interceptors import (
    add_error_interceptor,
    add_request_interceptor,
    add_response_interceptor,
    apply_error_interceptors,
    apply_request_interceptors,
    apply_response_interceptors,
)
from .logger import get_logger
from .plain_object import convert_to_plain_object
from .request_id import generate_request_id
from .retry import retry_api_call
from .url_utils import append_broker_filter_to_url, append_theme_to_url
from .validation import validate_params

__all__ = [
    "generate_request_id",
    "retry_api_call",
    "get_logger",
    "handle_error",
    "FinaticError",
    "ApiError",
    "ValidationError",
    "validate_params",
    "get_cache",
    "generate_cache_key",
    "add_request_interceptor",
    "add_response_interceptor",
    "add_error_interceptor",
    "apply_request_interceptors",
    "apply_response_interceptors",
    "apply_error_interceptors",
    "append_theme_to_url",
    "append_broker_filter_to_url",
    "coerce_enum_value",
    "convert_to_plain_object",
]
