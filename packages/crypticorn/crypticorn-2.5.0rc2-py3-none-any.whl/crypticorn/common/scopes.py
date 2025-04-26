from enum import StrEnum, EnumMeta
import logging

logger = logging.getLogger("uvicorn")


class Fallback(EnumMeta):
    """Fallback to no scope for unknown scopes."""

    # Note: This is a workaround to avoid the AttributeError when an unknown scope is accessed.
    # As soon as we have stable scopes, we can remove this.

    def __getattr__(cls, name):
        # Let Pydantic/internal stuff pass silently ! fragile
        if name.startswith("__"):
            raise AttributeError(name)
        logger.warning(
            f"Unknown scope '{name}' - falling back to no scope - update crypticorn package or check for typos"
        )
        return None


class Scope(StrEnum):
    """
    The permission scopes for the API.
    """

    # If you update anything here, also update the scopes in the auth-service repository

    @classmethod
    def from_str(cls, value: str) -> "Scope":
        return cls(value)

    # Scopes that can be purchased - these actually exist in the jwt token
    READ_PREDICTIONS = "read:predictions"

    # Hive scopes
    READ_HIVE_MODEL = "read:hive:model"
    READ_HIVE_DATA = "read:hive:data"
    WRITE_HIVE_MODEL = "write:hive:model"

    # Trade scopes
    READ_TRADE_BOTS = "read:trade:bots"
    WRITE_TRADE_BOTS = "write:trade:bots"
    READ_TRADE_EXCHANGEKEYS = "read:trade:exchangekeys"
    WRITE_TRADE_EXCHANGEKEYS = "write:trade:exchangekeys"
    READ_TRADE_ORDERS = "read:trade:orders"
    READ_TRADE_ACTIONS = "read:trade:actions"
    WRITE_TRADE_ACTIONS = "write:trade:actions"
    READ_TRADE_EXCHANGES = "read:trade:exchanges"
    READ_TRADE_FUTURES = "read:trade:futures"
    WRITE_TRADE_FUTURES = "write:trade:futures"
    READ_TRADE_NOTIFICATIONS = "read:trade:notifications"
    WRITE_TRADE_NOTIFICATIONS = "write:trade:notifications"
    READ_TRADE_STRATEGIES = "read:trade:strategies"
    WRITE_TRADE_STRATEGIES = "write:trade:strategies"

    # Payment scopes
    READ_PAY_PAYMENTS = "read:pay:payments"
    READ_PAY_PRODUCTS = "read:pay:products"
    WRITE_PAY_PRODUCTS = "write:pay:products"
    READ_PAY_NOW = "read:pay:now"
    WRITE_PAY_NOW = "write:pay:now"

    # Metrics scopes
    READ_METRICS_MARKETCAP = "read:metrics:marketcap"
    READ_METRICS_INDICATORS = "read:metrics:indicators"
    READ_METRICS_EXCHANGES = "read:metrics:exchanges"
    READ_METRICS_TOKENS = "read:metrics:tokens"
    READ_METRICS_MARKETS = "read:metrics:markets"
