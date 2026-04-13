"""Tests for custom extension modules that should survive regeneration."""

from __future__ import annotations

import importlib


def test_custom_finatic_server_subclasses_generated_base() -> None:
    custom_module = importlib.import_module("src.FinaticServer")
    generated_module = importlib.import_module("src.FinaticServerCore")

    custom_cls = custom_module.FinaticServer
    generated_cls = generated_module.FinaticServer

    assert getattr(custom_cls, "__CUSTOM_CLASS__", False) is True
    assert issubclass(custom_cls, generated_cls)


def test_wrappers_module_exports_expected_classes() -> None:
    session_module = importlib.import_module("src.wrappers.session")
    brokers_module = importlib.import_module("src.wrappers.brokers")

    assert hasattr(session_module, "SessionWrapper")
    assert hasattr(brokers_module, "BrokersWrapper")
