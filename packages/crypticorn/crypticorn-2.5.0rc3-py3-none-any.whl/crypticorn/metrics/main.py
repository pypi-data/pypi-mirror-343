from __future__ import annotations
from crypticorn.metrics import (
    ApiClient,
    Configuration,
    ExchangesApi,
    HealthCheckApi,
    IndicatorsApi,
    LogsApi,
    MarketcapApi,
    MarketsApi,
    TokensApi,
    MarketType,
)
from crypticorn.common import optional_import
from pydantic import StrictStr, StrictInt, Field
from typing_extensions import Annotated
from typing import Optional


class MetricsClient:
    """
    A client for interacting with the Crypticorn Metrics API.
    """

    def __init__(
        self,
        config: Configuration,
    ):
        self.config = config
        self.base_client = ApiClient(configuration=self.config)
        # Instantiate all the endpoint clients
        self.status = HealthCheckApi(self.base_client)
        self.indicators = IndicatorsApi(self.base_client)
        self.logs = LogsApi(self.base_client)
        self.marketcap = MarketcapApiWrapper(self.base_client)
        self.markets = MarketsApi(self.base_client)
        self.tokens = TokensApiWrapper(self.base_client)
        self.exchanges = ExchangesApi(self.base_client)


class MarketcapApiWrapper(MarketcapApi):
    """
    A wrapper for the MarketcapApi class.
    """

    async def get_marketcap_symbols_fmt(
        self,
        start_timestamp: Annotated[
            Optional[StrictInt], Field(description="Start timestamp")
        ] = None,
        end_timestamp: Annotated[
            Optional[StrictInt], Field(description="End timestamp")
        ] = None,
        interval: Annotated[
            Optional[StrictStr],
            Field(description="Interval for which to fetch symbols and marketcap data"),
        ] = None,
        market: Annotated[
            Optional[MarketType],
            Field(description="Market for which to fetch symbols and marketcap data"),
        ] = None,
        exchange: Annotated[
            Optional[StrictStr],
            Field(description="Exchange for which to fetch symbols and marketcap data"),
        ] = None,
    ) -> pd.DataFrame:
        """
        Get the marketcap symbols in a pandas dataframe
        """
        pd = optional_import("pandas", "extra")
        response = await self.get_marketcap_symbols(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            interval=interval,
            market=market,
            exchange=exchange,
        )
        json_response = await response.json()
        df = pd.DataFrame(json_response["data"])
        df.rename(columns={df.columns[0]: "timestamp"}, inplace=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"]).astype("int64") // 10**9
        return df


class TokensApiWrapper(TokensApi):
    """
    A wrapper for the TokensApi class.
    """

    async def get_tokens_fmt(
        self,
        token_type: Annotated[
            StrictStr,
            Field(description="Type of tokens to fetch"),
        ],
    ) -> pd.DataFrame:
        """
        Get the tokens in a pandas dataframe
        """
        pd = optional_import("pandas", "extra")
        response = await self.get_stable_and_wrapped_tokens_without_preload_content(
            token_type=token_type
        )
        json_data = await response.json()
        return pd.DataFrame(json_data["data"])
