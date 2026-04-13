"""Main SDK entry point."""

try:
    from .FinaticServer import FinaticServer
except ModuleNotFoundError:
    pass

try:
    from .openapi.generated import *  # type: ignore[F401,F403]
except ModuleNotFoundError:
    pass
