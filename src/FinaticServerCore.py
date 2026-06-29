"""Finatic Server SDK — thin bootstrap over ``finatic.v1``."""

from __future__ import annotations

from typing import Any

from finatic_server.api_client import ApiClient
from finatic_server.configuration import Configuration

from .config import SdkConfig, get_config
from .utils.logger import get_logger
from .v1 import V1Client


def _merge_sdk_config(sdk_config: SdkConfig | dict[str, Any] | None) -> SdkConfig:
    merged_config = get_config()
    if sdk_config is None:
        return merged_config
    if isinstance(sdk_config, SdkConfig):
        for field_name in sdk_config.__dataclass_fields__:
            setattr(merged_config, field_name, getattr(sdk_config, field_name))
        return merged_config
    for key, value in sdk_config.items():
        if hasattr(merged_config, key):
            setattr(merged_config, key, value)
    return merged_config


class FinaticServer:
    """Main client class for Finatic Server SDK."""

    def __init__(
        self,
        api_key: str,
        sdk_config: SdkConfig | dict[str, Any] | None = None,
    ) -> None:
        self.api_key = api_key
        self.sdk_config = _merge_sdk_config(sdk_config)
        self.logger = get_logger(self.sdk_config)

        configuration = Configuration(
            host=self.sdk_config.base_url,
            api_key={"X-API-Key": api_key},
        )
        api_client = ApiClient(configuration)
        self._v1 = V1Client(
            api_client=api_client,
            config=configuration,
            api_key=api_key,
            environment=self.sdk_config.environment,
        )

    @property
    def v1(self) -> V1Client:
        """Versioned v1 client for all API operations."""
        return self._v1

    @classmethod
    async def init(
        cls,
        api_key: str,
        user_id: str | None = None,
        sdk_config: SdkConfig | dict[str, Any] | None = None,
    ) -> FinaticServer:
        instance = cls(api_key, sdk_config)
        session_result = await instance.v1.start_session(user_id=user_id)
        if (
            isinstance(session_result, dict)
            and "success" in session_result
            and not session_result.get("success")
        ):
            error_message = session_result.get("error") or (
                "Session initialization failed. Check the API key and "
                "/api/v1/session/init + /start responses."
            )
            raise ValueError(str(error_message))
        if not instance.v1.get_session_id():
            raise ValueError("Session initialization failed: missing session_id.")
        return instance

    async def close(self) -> None:
        """Close the client and cleanup resources."""
        return
