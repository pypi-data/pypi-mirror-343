from crypticorn.hive import (
    ApiClient,
    Configuration,
    ModelsApi,
    DataApi,
    StatusApi,
    Configuration,
)
from crypticorn.common import apikey_header as aph


class HiveClient:
    """
    A client for interacting with the Crypticorn Hive API.
    """

    def __init__(
        self,
        config: Configuration,
    ):
        self.config = config
        self.base_client = ApiClient(configuration=self.config)
        # Instantiate all the endpoint clients
        self.models = ModelsApi(self.base_client)
        self.data = DataApi(self.base_client)
        self.status = StatusApi(self.base_client)
