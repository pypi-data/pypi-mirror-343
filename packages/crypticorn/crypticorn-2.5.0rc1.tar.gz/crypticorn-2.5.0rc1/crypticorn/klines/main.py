from __future__ import annotations
from crypticorn.klines import (
    ApiClient,
    Configuration,
    FundingRatesApi,
    HealthCheckApi,
    OHLCVDataApi,
    SymbolsApi,
    UDFApi,
)
from crypticorn.common import optional_import


class FundingRatesApiWrapper(FundingRatesApi):
    """
    A wrapper for the FundingRatesApi class.
    """

    def get_funding_rates_fmt(self) -> pd.DataFrame:
        pd = optional_import("pandas", "extra")
        response = self.funding_rate_funding_rates_symbol_get()
        return pd.DataFrame(response.json())


class OHLCVDataApiWrapper(OHLCVDataApi):
    """
    A wrapper for the OHLCVDataApi class.
    """

    def get_ohlcv_data_fmt(self) -> pd.DataFrame:
        pd = optional_import("pandas", "extra")
        response = self.get_ohlcv_market_timeframe_symbol_get()
        return pd.DataFrame(response.json())


class SymbolsApiWrapper(SymbolsApi):
    """
    A wrapper for the SymbolsApi class.
    """

    def get_symbols_fmt(self) -> pd.DataFrame:
        pd = optional_import("pandas", "extra")
        response = self.symbols_symbols_market_get()
        return pd.DataFrame(response.json())


class UDFApiWrapper(UDFApi):
    """
    A wrapper for the UDFApi class.
    """

    def get_udf_fmt(self) -> pd.DataFrame:
        pd = optional_import("pandas", "extra")
        response = self.get_history_udf_history_get()
        return pd.DataFrame(response.json())


class KlinesClient:
    """
    A client for interacting with the Crypticorn Klines API.
    """

    def __init__(
        self,
        config: Configuration,
    ):
        self.config = config
        self.base_client = ApiClient(configuration=self.config)
        # Instantiate all the endpoint clients
        self.funding = FundingRatesApiWrapper(self.base_client)
        self.ohlcv = OHLCVDataApiWrapper(self.base_client)
        self.symbols = SymbolsApiWrapper(self.base_client)
        self.udf = UDFApiWrapper(self.base_client)
        self.health = HealthCheckApi(self.base_client)
