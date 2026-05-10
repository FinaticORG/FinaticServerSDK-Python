"""Main SDK entry point."""

from .openapi import path_bootstrap  # noqa: F401

try:
    from .FinaticServer import FinaticServer
except ModuleNotFoundError:
    pass

try:
    from finatic_server import *  # type: ignore[F401,F403]
except ModuleNotFoundError:
    pass
