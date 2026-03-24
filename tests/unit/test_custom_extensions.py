"""Tests for custom extension modules that should survive regeneration."""

from __future__ import annotations

import importlib


def test_custom_finatic_server_subclasses_generated_base() -> None:
    custom_module = importlib.import_module("src.custom.FinaticServer")
    generated_module = importlib.import_module("src.generated.FinaticServer")

    custom_cls = custom_module.FinaticServer
    generated_cls = generated_module.FinaticServer

    assert getattr(custom_cls, "__CUSTOM_CLASS__", False) is True
    assert issubclass(custom_cls, generated_cls)


def test_custom_wrappers_subclass_generated_wrappers() -> None:
    custom_session_module = importlib.import_module("src.custom.wrappers.session")
    custom_brokers_module = importlib.import_module("src.custom.wrappers.brokers")
    generated_session_module = importlib.import_module("src.generated.wrappers.session")
    generated_brokers_module = importlib.import_module("src.generated.wrappers.brokers")

    assert issubclass(
        custom_session_module.CustomSessionWrapper,
        generated_session_module.SessionWrapper,
    )
    assert issubclass(
        custom_brokers_module.CustomBrokersWrapper,
        generated_brokers_module.BrokersWrapper,
    )
