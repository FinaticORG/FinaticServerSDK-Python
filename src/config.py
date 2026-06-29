"""Finatic Server SDK Configuration."""

import os
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SdkConfig:
    """SDK configuration with customizable options."""

    base_url: str = field(
        default_factory=lambda: os.getenv("FINATIC_API_URL", "https://api.finatic.dev")
    )
    api_key: str | None = field(default_factory=lambda: os.getenv("FINATIC_API_KEY"))
    timeout: int = field(
        default_factory=lambda: int(os.getenv("FINATIC_TIMEOUT", "30"))
    )
    headers: dict[str, str] = field(default_factory=dict)
    environment: str = field(
        default_factory=lambda: os.getenv("FINATIC_ENVIRONMENT", "live")
    )

    log_level: str = field(
        default_factory=lambda: os.getenv("FINATIC_LOG_LEVEL", "error")
    )
    structured_logging: bool = field(
        default_factory=lambda: (
            os.getenv("FINATIC_STRUCTURED_LOGGING", "false").lower() == "true"
        )
    )
    log_request_body: bool = field(
        default_factory=lambda: (
            os.getenv("FINATIC_LOG_REQUEST_BODY", "false").lower() == "true"
        )
    )
    log_response_body: bool = field(
        default_factory=lambda: (
            os.getenv("FINATIC_LOG_RESPONSE_BODY", "false").lower() == "true"
        )
    )
    log_request_id: bool = field(
        default_factory=lambda: (
            os.getenv("FINATIC_LOG_REQUEST_ID", "true").lower() != "false"
        )
    )

    validation_enabled: bool = field(
        default_factory=lambda: (
            os.getenv("FINATIC_VALIDATION_ENABLED", "true").lower() != "false"
        )
    )
    validation_strict: bool = field(
        default_factory=lambda: (
            os.getenv("FINATIC_VALIDATION_STRICT", "false").lower() == "true"
        )
    )

    session_context_storage: str = field(
        default_factory=lambda: os.getenv("FINATIC_SESSION_STORAGE", "memory")
    )
    session_context_getter: Callable[[], dict[str, str | None]] | None = None
    session_context_setter: Callable[[dict[str, str | None]], None] | None = None


def get_config(overrides: dict[str, Any] | None = None) -> SdkConfig:
    """Get configuration with optional overrides."""
    config = SdkConfig()

    if overrides:
        for key, value in overrides.items():
            if hasattr(config, key):
                setattr(config, key, value)

    return config
