from enum import Enum, EnumMeta, StrEnum
import logging
from fastapi import status

logger = logging.getLogger(__name__)


class Fallback(EnumMeta):
    """Fallback to UNKNOWN_ERROR for error codes not yet published to PyPI."""

    def __getattr__(cls, name):
        # Let Pydantic/internal stuff pass silently ! fragile
        if name.startswith("__"):
            raise AttributeError(name)
        logger.warning(
            f"Unknown error code '{name}' - update crypticorn package or check for typos"
        )
        return cls.UNKNOWN_ERROR


class ApiErrorType(StrEnum):
    """Type of API error"""

    USER_ERROR = "user error"
    """user error by people using our services"""
    EXCHANGE_ERROR = "exchange error"
    """re-tryable error by the exchange or network conditions"""
    SERVER_ERROR = "server error"
    """server error that needs a new version rollout for a fix"""
    NO_ERROR = "no error"
    """error that does not need to be handled or does not affect the program or is a placeholder."""


class ApiErrorIdentifier(StrEnum):
    """API error identifiers"""

    ALLOCATION_BELOW_EXPOSURE = "allocation_below_current_exposure"
    ALLOCATION_BELOW_MINIMUM = "allocation_below_min_amount"
    BLACK_SWAN = "black_swan"
    BOT_ALREADY_DELETED = "bot_already_deleted"
    BOT_DISABLED = "bot_disabled"
    BOT_STOPPING_COMPLETED = "bot_stopping_completed"
    CLIENT_ORDER_ID_REPEATED = "client_order_id_already_exists"
    CONTENT_TYPE_ERROR = "invalid_content_type"
    DELETE_BOT_ERROR = "delete_bot_error"
    EXCHANGE_INVALID_SIGNATURE = "exchange_invalid_signature"
    EXCHANGE_INVALID_TIMESTAMP = "exchange_invalid_timestamp"
    EXCHANGE_IP_RESTRICTED = "exchange_ip_address_is_not_authorized"
    EXCHANGE_KEY_ALREADY_EXISTS = "exchange_key_already_exists"
    EXCHANGE_KEY_IN_USE = "exchange_key_in_use"
    EXCHANGE_MAINTENANCE = "exchange_system_under_maintenance"
    EXCHANGE_RATE_LIMIT = "exchange_rate_limit_exceeded"
    EXCHANGE_PERMISSION_DENIED = "insufficient_permissions_spot_and_futures_required"
    EXCHANGE_SERVICE_UNAVAILABLE = "exchange_service_temporarily_unavailable"
    EXCHANGE_SYSTEM_BUSY = "exchange_system_is_busy"
    EXCHANGE_SYSTEM_CONFIG_ERROR = "exchange_system_configuration_error"
    EXCHANGE_SYSTEM_ERROR = "exchange_internal_system_error"
    EXCHANGE_USER_FROZEN = "exchange_user_account_is_frozen"
    HEDGE_MODE_NOT_ACTIVE = "hedge_mode_not_active"
    HTTP_ERROR = "http_request_error"
    INSUFFICIENT_BALANCE = "insufficient_balance"
    INSUFFICIENT_MARGIN = "insufficient_margin"
    INSUFFICIENT_SCOPES = "insufficient_scopes"
    INVALID_API_KEY = "invalid_api_key"
    INVALID_BEARER = "invalid_bearer"
    INVALID_EXCHANGE_KEY = "invalid_exchange_key"
    INVALID_MARGIN_MODE = "invalid_margin_mode"
    INVALID_PARAMETER = "invalid_parameter_provided"
    JWT_EXPIRED = "jwt_expired"
    LEVERAGE_EXCEEDED = "leverage_limit_exceeded"
    LIQUIDATION_PRICE_VIOLATION = "order_violates_liquidation_price_constraints"
    NO_CREDENTIALS = "no_credentials"
    NOW_API_DOWN = "now_api_down"
    OBJECT_NOT_FOUND = "object_not_found"
    OBJECT_ALREADY_EXISTS = "object_already_exists"
    ORDER_ALREADY_FILLED = "order_is_already_filled"
    ORDER_IN_PROCESS = "order_is_being_processed"
    ORDER_LIMIT_EXCEEDED = "order_quantity_limit_exceeded"
    ORDER_NOT_FOUND = "order_does_not_exist"
    ORDER_PRICE_INVALID = "order_price_is_invalid"
    ORDER_SIZE_TOO_LARGE = "order_size_too_large"
    ORDER_SIZE_TOO_SMALL = "order_size_too_small"
    POSITION_LIMIT_EXCEEDED = "position_limit_exceeded"
    POSITION_NOT_FOUND = "position_does_not_exist"
    POSITION_SUSPENDED = "position_opening_temporarily_suspended"
    POST_ONLY_REJECTED = "post_only_order_would_immediately_match"
    REQUEST_SCOPE_EXCEEDED = "request_scope_limit_exceeded"
    RISK_LIMIT_EXCEEDED = "risk_limit_exceeded"
    RPC_TIMEOUT = "rpc_timeout"
    SETTLEMENT_IN_PROGRESS = "system_settlement_in_process"
    STRATEGY_DISABLED = "strategy_disabled"
    STRATEGY_LEVERAGE_MISMATCH = "strategy_leverage_mismatch"
    STRATEGY_NOT_SUPPORTING_EXCHANGE = "strategy_not_supporting_exchange"
    SUCCESS = "success"
    SYMBOL_NOT_FOUND = "symbol_does_not_exist"
    TRADING_ACTION_EXPIRED = "trading_action_expired"
    TRADING_ACTION_SKIPPED = "trading_action_skipped"
    TRADING_LOCKED = "trading_has_been_locked"
    TRADING_SUSPENDED = "trading_is_suspended"
    UNKNOWN_ERROR = "unknown_error_occurred"
    URL_NOT_FOUND = "requested_resource_not_found"

    @property
    def get_error_code(self) -> str:
        """Get the corresponding ApiError."""
        return ApiError[self.value]


class ApiErrorLevel(StrEnum):
    """API error levels"""

    ERROR = "error"
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"


class ApiError(Enum, metaclass=Fallback):
    """API error codes. Fallback to UNKNOWN_ERROR for error codes not yet published to PyPI."""

    ALLOCATION_BELOW_EXPOSURE = (
        ApiErrorIdentifier.ALLOCATION_BELOW_EXPOSURE,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    ALLOCATION_BELOW_MINIMUM = (
        ApiErrorIdentifier.ALLOCATION_BELOW_MINIMUM,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    BLACK_SWAN = (
        ApiErrorIdentifier.BLACK_SWAN,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.INFO,
    )
    BOT_ALREADY_DELETED = (
        ApiErrorIdentifier.BOT_ALREADY_DELETED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    BOT_DISABLED = (
        ApiErrorIdentifier.BOT_DISABLED,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.WARNING,
    )
    BOT_STOPPING_COMPLETED = (
        ApiErrorIdentifier.BOT_STOPPING_COMPLETED,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )
    CLIENT_ORDER_ID_REPEATED = (
        ApiErrorIdentifier.CLIENT_ORDER_ID_REPEATED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    CONTENT_TYPE_ERROR = (
        ApiErrorIdentifier.CONTENT_TYPE_ERROR,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    DELETE_BOT_ERROR = (
        ApiErrorIdentifier.DELETE_BOT_ERROR,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_INVALID_SIGNATURE = (
        ApiErrorIdentifier.EXCHANGE_INVALID_SIGNATURE,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_INVALID_TIMESTAMP = (
        ApiErrorIdentifier.EXCHANGE_INVALID_TIMESTAMP,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_IP_RESTRICTED = (
        ApiErrorIdentifier.EXCHANGE_IP_RESTRICTED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_KEY_ALREADY_EXISTS = (
        ApiErrorIdentifier.EXCHANGE_KEY_ALREADY_EXISTS,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_KEY_IN_USE = (
        ApiErrorIdentifier.EXCHANGE_KEY_IN_USE,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_MAINTENANCE = (
        ApiErrorIdentifier.EXCHANGE_MAINTENANCE,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_RATE_LIMIT = (
        ApiErrorIdentifier.EXCHANGE_RATE_LIMIT,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_PERMISSION_DENIED = (
        ApiErrorIdentifier.EXCHANGE_PERMISSION_DENIED,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_SERVICE_UNAVAILABLE = (
        ApiErrorIdentifier.EXCHANGE_SERVICE_UNAVAILABLE,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_SYSTEM_BUSY = (
        ApiErrorIdentifier.EXCHANGE_SYSTEM_BUSY,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_SYSTEM_CONFIG_ERROR = (
        ApiErrorIdentifier.EXCHANGE_SYSTEM_CONFIG_ERROR,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_SYSTEM_ERROR = (
        ApiErrorIdentifier.EXCHANGE_SYSTEM_ERROR,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    EXCHANGE_USER_FROZEN = (
        ApiErrorIdentifier.EXCHANGE_USER_FROZEN,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    HEDGE_MODE_NOT_ACTIVE = (
        ApiErrorIdentifier.HEDGE_MODE_NOT_ACTIVE,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    HTTP_ERROR = (
        ApiErrorIdentifier.HTTP_ERROR,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    INSUFFICIENT_BALANCE = (
        ApiErrorIdentifier.INSUFFICIENT_BALANCE,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INSUFFICIENT_MARGIN = (
        ApiErrorIdentifier.INSUFFICIENT_MARGIN,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INSUFFICIENT_SCOPES = (
        ApiErrorIdentifier.INSUFFICIENT_SCOPES,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INVALID_API_KEY = (
        ApiErrorIdentifier.INVALID_API_KEY,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INVALID_BEARER = (
        ApiErrorIdentifier.INVALID_BEARER,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INVALID_EXCHANGE_KEY = (
        ApiErrorIdentifier.INVALID_EXCHANGE_KEY,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INVALID_MARGIN_MODE = (
        ApiErrorIdentifier.INVALID_MARGIN_MODE,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    INVALID_PARAMETER = (
        ApiErrorIdentifier.INVALID_PARAMETER,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    JWT_EXPIRED = (
        ApiErrorIdentifier.JWT_EXPIRED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    LEVERAGE_EXCEEDED = (
        ApiErrorIdentifier.LEVERAGE_EXCEEDED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    LIQUIDATION_PRICE_VIOLATION = (
        ApiErrorIdentifier.LIQUIDATION_PRICE_VIOLATION,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    NO_CREDENTIALS = (
        ApiErrorIdentifier.NO_CREDENTIALS,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    NOW_API_DOWN = (
        ApiErrorIdentifier.NOW_API_DOWN,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    OBJECT_NOT_FOUND = (
        ApiErrorIdentifier.OBJECT_NOT_FOUND,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    OBJECT_ALREADY_EXISTS = (
        ApiErrorIdentifier.OBJECT_ALREADY_EXISTS,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    ORDER_ALREADY_FILLED = (
        ApiErrorIdentifier.ORDER_ALREADY_FILLED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.INFO,
    )
    ORDER_IN_PROCESS = (
        ApiErrorIdentifier.ORDER_IN_PROCESS,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )
    ORDER_LIMIT_EXCEEDED = (
        ApiErrorIdentifier.ORDER_LIMIT_EXCEEDED,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    ORDER_NOT_FOUND = (
        ApiErrorIdentifier.ORDER_NOT_FOUND,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    ORDER_PRICE_INVALID = (
        ApiErrorIdentifier.ORDER_PRICE_INVALID,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    ORDER_SIZE_TOO_LARGE = (
        ApiErrorIdentifier.ORDER_SIZE_TOO_LARGE,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.WARNING,
    )
    ORDER_SIZE_TOO_SMALL = (
        ApiErrorIdentifier.ORDER_SIZE_TOO_SMALL,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.WARNING,
    )
    POSITION_LIMIT_EXCEEDED = (
        ApiErrorIdentifier.POSITION_LIMIT_EXCEEDED,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    POSITION_NOT_FOUND = (
        ApiErrorIdentifier.POSITION_NOT_FOUND,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )
    POSITION_SUSPENDED = (
        ApiErrorIdentifier.POSITION_SUSPENDED,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    POST_ONLY_REJECTED = (
        ApiErrorIdentifier.POST_ONLY_REJECTED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    REQUEST_SCOPE_EXCEEDED = (
        ApiErrorIdentifier.REQUEST_SCOPE_EXCEEDED,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    RISK_LIMIT_EXCEEDED = (
        ApiErrorIdentifier.RISK_LIMIT_EXCEEDED,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    RPC_TIMEOUT = (
        ApiErrorIdentifier.RPC_TIMEOUT,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    SETTLEMENT_IN_PROGRESS = (
        ApiErrorIdentifier.SETTLEMENT_IN_PROGRESS,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    STRATEGY_DISABLED = (
        ApiErrorIdentifier.STRATEGY_DISABLED,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    STRATEGY_LEVERAGE_MISMATCH = (
        ApiErrorIdentifier.STRATEGY_LEVERAGE_MISMATCH,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    STRATEGY_NOT_SUPPORTING_EXCHANGE = (
        ApiErrorIdentifier.STRATEGY_NOT_SUPPORTING_EXCHANGE,
        ApiErrorType.USER_ERROR,
        ApiErrorLevel.ERROR,
    )
    SUCCESS = (ApiErrorIdentifier.SUCCESS, ApiErrorType.NO_ERROR, ApiErrorLevel.SUCCESS)
    SYMBOL_NOT_FOUND = (
        ApiErrorIdentifier.SYMBOL_NOT_FOUND,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )
    TRADING_ACTION_EXPIRED = (
        ApiErrorIdentifier.TRADING_ACTION_EXPIRED,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )
    TRADING_ACTION_SKIPPED = (
        ApiErrorIdentifier.TRADING_ACTION_SKIPPED,
        ApiErrorType.NO_ERROR,
        ApiErrorLevel.INFO,
    )
    TRADING_LOCKED = (
        ApiErrorIdentifier.TRADING_LOCKED,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    TRADING_SUSPENDED = (
        ApiErrorIdentifier.TRADING_SUSPENDED,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    UNKNOWN_ERROR = (
        ApiErrorIdentifier.UNKNOWN_ERROR,
        ApiErrorType.EXCHANGE_ERROR,
        ApiErrorLevel.ERROR,
    )
    URL_NOT_FOUND = (
        ApiErrorIdentifier.URL_NOT_FOUND,
        ApiErrorType.SERVER_ERROR,
        ApiErrorLevel.ERROR,
    )

    @property
    def identifier(self) -> str:
        """Identifier of the error."""
        return self.value[0]

    @property
    def type(self) -> ApiErrorType:
        """Type of the error."""
        return self.value[1]

    @property
    def level(self) -> ApiErrorLevel:
        """Level of the error."""
        return self.value[2]

    @property
    def status_code(self) -> int:
        """HTTP status code for the error."""
        return HttpStatusMapper.get_status_code(self)


class HttpStatusMapper:
    """Map API errors to HTTP status codes."""

    # TODO: decide if we need all of these mappings, since most errors are not exposed to the client via HTTP
    # in case we remove some, update the pytest length check
    _mapping = {
        # Authentication/Authorization
        ApiError.JWT_EXPIRED: status.HTTP_401_UNAUTHORIZED,
        ApiError.INVALID_BEARER: status.HTTP_401_UNAUTHORIZED,
        ApiError.INVALID_API_KEY: status.HTTP_401_UNAUTHORIZED,
        ApiError.NO_CREDENTIALS: status.HTTP_401_UNAUTHORIZED,
        ApiError.INSUFFICIENT_SCOPES: status.HTTP_403_FORBIDDEN,
        ApiError.EXCHANGE_PERMISSION_DENIED: status.HTTP_403_FORBIDDEN,
        ApiError.EXCHANGE_USER_FROZEN: status.HTTP_403_FORBIDDEN,
        ApiError.TRADING_LOCKED: status.HTTP_403_FORBIDDEN,
        # Not Found
        ApiError.URL_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ApiError.OBJECT_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ApiError.ORDER_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ApiError.POSITION_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        ApiError.SYMBOL_NOT_FOUND: status.HTTP_404_NOT_FOUND,
        # Conflicts/Duplicates
        ApiError.CLIENT_ORDER_ID_REPEATED: status.HTTP_409_CONFLICT,
        ApiError.OBJECT_ALREADY_EXISTS: status.HTTP_409_CONFLICT,
        ApiError.EXCHANGE_KEY_ALREADY_EXISTS: status.HTTP_409_CONFLICT,
        ApiError.BOT_ALREADY_DELETED: status.HTTP_409_CONFLICT,
        # Invalid Content
        ApiError.CONTENT_TYPE_ERROR: status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        # Rate Limits
        ApiError.EXCHANGE_RATE_LIMIT: status.HTTP_429_TOO_MANY_REQUESTS,
        ApiError.REQUEST_SCOPE_EXCEEDED: status.HTTP_429_TOO_MANY_REQUESTS,
        # Server Errors
        ApiError.UNKNOWN_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
        ApiError.EXCHANGE_SYSTEM_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
        ApiError.NOW_API_DOWN: status.HTTP_500_INTERNAL_SERVER_ERROR,
        ApiError.RPC_TIMEOUT: status.HTTP_500_INTERNAL_SERVER_ERROR,
        # Service Unavailable
        ApiError.EXCHANGE_SERVICE_UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,
        ApiError.EXCHANGE_MAINTENANCE: status.HTTP_503_SERVICE_UNAVAILABLE,
        ApiError.EXCHANGE_SYSTEM_BUSY: status.HTTP_503_SERVICE_UNAVAILABLE,
        ApiError.SETTLEMENT_IN_PROGRESS: status.HTTP_503_SERVICE_UNAVAILABLE,
        ApiError.POSITION_SUSPENDED: status.HTTP_503_SERVICE_UNAVAILABLE,
        ApiError.TRADING_SUSPENDED: status.HTTP_503_SERVICE_UNAVAILABLE,
        # Bad Requests (400) - Invalid parameters or states
        ApiError.ALLOCATION_BELOW_EXPOSURE: status.HTTP_400_BAD_REQUEST,
        ApiError.ALLOCATION_BELOW_MINIMUM: status.HTTP_400_BAD_REQUEST,
        ApiError.BLACK_SWAN: status.HTTP_400_BAD_REQUEST,
        ApiError.BOT_DISABLED: status.HTTP_400_BAD_REQUEST,
        ApiError.DELETE_BOT_ERROR: status.HTTP_400_BAD_REQUEST,
        ApiError.EXCHANGE_INVALID_SIGNATURE: status.HTTP_400_BAD_REQUEST,
        ApiError.EXCHANGE_INVALID_TIMESTAMP: status.HTTP_400_BAD_REQUEST,
        ApiError.EXCHANGE_IP_RESTRICTED: status.HTTP_400_BAD_REQUEST,
        ApiError.EXCHANGE_KEY_IN_USE: status.HTTP_400_BAD_REQUEST,
        ApiError.EXCHANGE_SYSTEM_CONFIG_ERROR: status.HTTP_400_BAD_REQUEST,
        ApiError.HEDGE_MODE_NOT_ACTIVE: status.HTTP_400_BAD_REQUEST,
        ApiError.HTTP_ERROR: status.HTTP_400_BAD_REQUEST,
        ApiError.INSUFFICIENT_BALANCE: status.HTTP_400_BAD_REQUEST,
        ApiError.INSUFFICIENT_MARGIN: status.HTTP_400_BAD_REQUEST,
        ApiError.INVALID_EXCHANGE_KEY: status.HTTP_400_BAD_REQUEST,
        ApiError.INVALID_MARGIN_MODE: status.HTTP_400_BAD_REQUEST,
        ApiError.INVALID_PARAMETER: status.HTTP_400_BAD_REQUEST,
        ApiError.LEVERAGE_EXCEEDED: status.HTTP_400_BAD_REQUEST,
        ApiError.LIQUIDATION_PRICE_VIOLATION: status.HTTP_400_BAD_REQUEST,
        ApiError.ORDER_ALREADY_FILLED: status.HTTP_400_BAD_REQUEST,
        ApiError.ORDER_IN_PROCESS: status.HTTP_400_BAD_REQUEST,
        ApiError.ORDER_LIMIT_EXCEEDED: status.HTTP_400_BAD_REQUEST,
        ApiError.ORDER_PRICE_INVALID: status.HTTP_400_BAD_REQUEST,
        ApiError.ORDER_SIZE_TOO_LARGE: status.HTTP_400_BAD_REQUEST,
        ApiError.ORDER_SIZE_TOO_SMALL: status.HTTP_400_BAD_REQUEST,
        ApiError.POSITION_LIMIT_EXCEEDED: status.HTTP_400_BAD_REQUEST,
        ApiError.POST_ONLY_REJECTED: status.HTTP_400_BAD_REQUEST,
        ApiError.RISK_LIMIT_EXCEEDED: status.HTTP_400_BAD_REQUEST,
        ApiError.STRATEGY_DISABLED: status.HTTP_400_BAD_REQUEST,
        ApiError.STRATEGY_LEVERAGE_MISMATCH: status.HTTP_400_BAD_REQUEST,
        ApiError.STRATEGY_NOT_SUPPORTING_EXCHANGE: status.HTTP_400_BAD_REQUEST,
        ApiError.TRADING_ACTION_EXPIRED: status.HTTP_400_BAD_REQUEST,
        ApiError.TRADING_ACTION_SKIPPED: status.HTTP_400_BAD_REQUEST,
        # Success cases
        ApiError.SUCCESS: status.HTTP_200_OK,
        ApiError.BOT_STOPPING_COMPLETED: status.HTTP_200_OK,
    }

    @classmethod
    def get_status_code(cls, error: ApiError) -> int:
        """Get the HTTP status code for the error. If the error is not in the mapping, return 500."""
        return cls._mapping.get(error, status.HTTP_500_INTERNAL_SERVER_ERROR)
