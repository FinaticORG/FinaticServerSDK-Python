"""Unit tests for generated SDK utils (coverage-focused)."""

from __future__ import annotations

from enum import Enum

import pytest
from pydantic import BaseModel, Field

from src.generated.config import SdkConfig
from src.generated.utils import enum_coercion
from src.generated.utils import plain_object
from src.generated.utils import url_utils
from src.generated.utils import validation
from src.generated.utils.error_handling import ValidationError as SdkValidationError


class _SampleEnum(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


def test_append_theme_and_broker_urls() -> None:
    assert url_utils.append_theme_to_url("https://example.com", None) == "https://example.com"
    out = url_utils.append_theme_to_url("https://example.com/path", "dark")
    assert "theme=dark" in out
    out2 = url_utils.append_theme_to_url(
        "https://example.com",
        {"preset": "solarized"},
    )
    assert "theme=solarized" in out2
    out3 = url_utils.append_theme_to_url(
        "https://example.com",
        {"custom": {"a": 1}},
    )
    assert "theme=custom" in out3 and "themeObject=" in out3
    # urlparse is permissive; ensure we still get a string with theme applied.
    odd = url_utils.append_theme_to_url("not-a-valid-scheme", "x")
    assert isinstance(odd, str) and "theme=" in odd

    brokers = url_utils.append_broker_filter_to_url(
        "https://example.com",
        ["alpaca"],
    )
    assert "brokers=" in brokers
    assert url_utils.append_kind_to_url("https://example.com", "broker") != "https://example.com"
    caps = url_utils.append_asset_types_to_url(
        "https://example.com",
        ["equity", "crypto"],
    )
    assert "capabilities=" in caps
    staged = url_utils.append_stage_to_url("https://example.com", ["production"])
    assert "stage=" in staged


def test_coerce_enum_value() -> None:
    assert enum_coercion.coerce_enum_value(None, _SampleEnum, "s") is None
    assert enum_coercion.coerce_enum_value(_SampleEnum.OPEN, _SampleEnum, "s") == _SampleEnum.OPEN
    assert enum_coercion.coerce_enum_value("OPEN", _SampleEnum, "s") == _SampleEnum.OPEN
    assert enum_coercion.coerce_enum_value("open", _SampleEnum, "s") == _SampleEnum.OPEN
    with pytest.raises(ValueError):
        enum_coercion.coerce_enum_value("nope", _SampleEnum, "status")


def test_convert_to_plain_object() -> None:
    assert plain_object.convert_to_plain_object(None) is None
    assert plain_object.convert_to_plain_object([1, {"a": 2}]) == [1, {"a": 2}]
    assert plain_object.convert_to_plain_object(_SampleEnum.CLOSED) == "closed"

    class _M(BaseModel):
        x: int = Field(default=1)

    dumped = plain_object.convert_to_plain_object(_M(x=2))
    assert dumped == {"x": 2}

    union_like = {
        "actual_instance": {"k": "v"},
        "any_of_schemas": True,
    }
    assert plain_object.convert_to_plain_object(union_like) == {"k": "v"}


def test_validate_params_paths() -> None:
    class _P(BaseModel):
        name: str

    cfg_off = SdkConfig(validation_enabled=False)
    out = validation.validate_params(_P, {"name": "a"}, cfg_off)
    assert out.name == "a"

    cfg_on = SdkConfig(validation_enabled=True, validation_strict=False)
    out_ok = validation.validate_params(_P, {"name": "ok"}, cfg_on)
    assert out_ok.name == "ok"

    cfg_strict = SdkConfig(validation_enabled=True, validation_strict=True)
    with pytest.raises(SdkValidationError):
        validation.validate_params(_P, {"name": 123}, cfg_strict)  # type: ignore[arg-type]
