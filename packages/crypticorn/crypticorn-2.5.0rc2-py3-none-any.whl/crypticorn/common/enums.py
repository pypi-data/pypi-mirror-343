from enum import StrEnum


class ValidateEnumMixin:
    """
    Mixin for validating enum values manually.

    ⚠️ Note:
    This does NOT enforce validation automatically on enum creation.
    It's up to the developer to call `Class.validate(value)` where needed.

    Usage:
        >>> class Color(ValidateEnumMixin, StrEnum):
        >>>     RED = "red"
        >>>     GREEN = "green"

        >>> Color.validate("red")     # True
        >>> Color.validate("yellow")  # False

    Order of inheritance matters — the mixin must come first.
    """

    @classmethod
    def validate(cls, value) -> bool:
        try:
            cls(value)
            return True
        except ValueError:
            return False


class Exchange(ValidateEnumMixin, StrEnum):
    """Supported exchanges for trading"""

    KUCOIN = "kucoin"
    BINGX = "bingx"


class InternalExchange(ValidateEnumMixin, StrEnum):
    """All exchanges we are using, including public (Exchange)"""

    KUCOIN = "kucoin"
    BINGX = "bingx"
    BINANCE = "binance"
    BYBIT = "bybit"
    HYPERLIQUID = "hyperliquid"
    BITGET = "bitget"


class MarketType(ValidateEnumMixin, StrEnum):
    """
    Market types
    """

    SPOT = "spot"
    FUTURES = "futures"
