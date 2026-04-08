"""Main SDK entry point.

This file is protected - customize exports as needed.
"""

# Re-export all other custom code (wrappers, utils, etc.)
# Re-export main client class explicitly (custom version that extends generated class)
# MUST come before export * from './custom' to ensure custom version is used
try:
    from .custom import *  # type: ignore[F401,F403]
    from .custom import FinaticServer
except ModuleNotFoundError:
    # Some local checkouts can have partially generated trees; allow importing
    # subpackages like src.generated.models without hard-failing package init.
    pass

# Re-export all generated code
try:
    from .generated import *  # type: ignore[F401,F403]
except ModuleNotFoundError:
    pass
