"""Hand-authored FinaticServer extension."""

from .FinaticServerCore import FinaticServer as GeneratedFinaticServer


class FinaticServer(GeneratedFinaticServer):
    """Hand-authored FinaticServer class."""

    __CUSTOM_CLASS__ = True
