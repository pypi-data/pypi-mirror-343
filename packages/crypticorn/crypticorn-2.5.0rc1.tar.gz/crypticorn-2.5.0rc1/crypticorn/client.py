from typing import Union

from crypticorn.hive import HiveClient, Configuration as HiveConfig
from crypticorn.klines import KlinesClient, Configuration as KlinesConfig
from crypticorn.pay import PayClient, Configuration as PayConfig
from crypticorn.trade import TradeClient, Configuration as TradeConfig
from crypticorn.metrics import MetricsClient, Configuration as MetricsConfig
from crypticorn.auth import AuthClient, Configuration as AuthConfig
from crypticorn.common import BaseUrl, ApiVersion, Service, apikey_header as aph
import warnings


class ApiClient:
    """
    The official client for interacting with the Crypticorn API.

    It is consisting of multiple microservices covering the whole stack of the Crypticorn project.
    """

    def __init__(
        self,
        api_key: str = None,
        jwt: str = None,
        base_url: BaseUrl = BaseUrl.PROD,
    ):
        self.base_url = base_url
        """The base URL the client will use to connect to the API."""
        self.api_key = api_key
        """The API key to use for authentication."""
        self.jwt = jwt
        """The JWT to use for authentication."""

        self.hive = HiveClient(self._get_default_config(Service.HIVE))
        self.trade = TradeClient(self._get_default_config(Service.TRADE))
        self.klines = KlinesClient(self._get_default_config(Service.KLINES))
        self.pay = PayClient(self._get_default_config(Service.PAY))
        self.metrics = MetricsClient(self._get_default_config(Service.METRICS))
        self.auth = AuthClient(self._get_default_config(Service.AUTH))

    def __new__(cls, *args, **kwargs):
        if kwargs.get("api_key") and not kwargs.get("jwt"):
            # auth-service does not allow api_key
            warnings.warn(
                "The auth module does only accept JWT to be used to authenticate. If you use this module, you need to provide a JWT."
            )
        return super().__new__(cls)

    async def close(self):
        """Close all client sessions."""
        clients = [
            self.hive.base_client,
            self.trade.base_client,
            self.klines.base_client,
            self.pay.base_client,
            self.metrics.base_client,
            self.auth.base_client,
        ]

        for client in clients:
            if hasattr(client, "close"):
                await client.close()

    def _get_default_config(
        self, service: Service, version: ApiVersion = ApiVersion.V1
    ):
        """
        Get the default configuration for a given service.
        """
        config_class = {
            Service.HIVE: HiveConfig,
            Service.TRADE: TradeConfig,
            Service.KLINES: KlinesConfig,
            Service.PAY: PayConfig,
            Service.METRICS: MetricsConfig,
            Service.AUTH: AuthConfig,
        }[service]
        return config_class(
            host=f"{self.base_url}/{version}/{service}",
            access_token=self.jwt,
            api_key={aph.scheme_name: self.api_key} if self.api_key else None,
            # not necessary
            # api_key_prefix=(
            #     {aph.scheme_name: aph.model.name} if self.api_key else None
            # ),
        )

    def configure(
        self,
        config: Union[
            HiveConfig, TradeConfig, KlinesConfig, PayConfig, MetricsConfig, AuthConfig
        ],
        sub_client: any,
    ):
        """
        Update a sub-client's configuration by overriding with the values set in the new config.
        Useful for testing a specific service against a local server instead of the default proxy.

        :param config: The new configuration to use for the sub-client.
        :param sub_client: The sub-client to configure.

        Example:
        This will override the host for the Hive client to connect to http://localhost:8000 instead of the default proxy:
        >>> async with ApiClient(base_url=BaseUrl.DEV, jwt=jwt) as client:
        >>>     client.configure(config=HiveConfig(host="http://localhost:8000"), sub_client=client.hive)
        """
        new_config = sub_client.config
        for attr in vars(config):
            new_value = getattr(config, attr)
            if new_value:
                setattr(new_config, attr, new_value)

        if sub_client == self.hive:
            self.hive = HiveClient(new_config)
        elif sub_client == self.trade:
            self.trade = TradeClient(new_config)
        elif sub_client == self.klines:
            self.klines = KlinesClient(new_config)
        elif sub_client == self.pay:
            self.pay = PayClient(new_config)
        elif sub_client == self.metrics:
            self.metrics = MetricsClient(new_config)
        elif sub_client == self.auth:
            self.auth = AuthClient(new_config)
        else:
            raise ValueError(f"Unknown sub-client: {sub_client}")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
