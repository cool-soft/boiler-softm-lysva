from typing import Optional, BinaryIO

import pandas as pd
import requests
from boiler.temp_graph.io.abstract_sync_temp_graph_loader import AbstractSyncTempGraphLoader
from boiler.temp_graph.io.abstract_sync_temp_graph_reader import AbstractSyncTempGraphReader

from boiler_softm_lysva.constants import api_constants, converting_parameters
from boiler_softm_lysva.logging import logger


class SoftMLysvaSyncTempGraphOnlineLoader(AbstractSyncTempGraphLoader):

    def __init__(self,
                 reader: AbstractSyncTempGraphReader,
                 api_base: str = api_constants.API_BASE,
                 http_proxy: Optional[str] = None,
                 https_proxy: Optional[str] = None
                 ) -> None:
        self._temp_graph_reader = reader
        self._api_base = api_base
        self._proxies = {}
        if http_proxy is not None:
            self._proxies.update({"http": http_proxy})
        if https_proxy is not None:
            self._proxies.update({"https": https_proxy})

        logger.debug(
            f"Creating instance: "
            f"reader: {self._temp_graph_reader} "
            f"api_base: {self._api_base} "
            f"http_proxy: {http_proxy} "
        )

    def load_temp_graph(self) -> pd.DataFrame:
        logger.debug("Loading temp graph")
        url = f"{self._api_base}/JSON"
        params = {
            "method": "getTempGraphic"
        }
        with requests.get(url=url, params=params, proxies=self._proxies, stream=True) as response:
            logger.debug(f"Temp graph is loaded from server. Status code is {response.status_code}")
            temp_graph_df = self._temp_graph_reader.read_temp_graph_from_binary_stream(response.raw)
        return temp_graph_df


class SoftMLysvaSyncTempGraphOnlineReader(AbstractSyncTempGraphReader):

    def __init__(self, encoding: str = "utf-8") -> None:
        self._encoding = encoding
        self._column_names_equal = converting_parameters.TEMP_GRAPH_COLUMN_NAMES_EQUALS
        logger.debug(f"Creating instance. Encoding: {encoding}")

    def read_temp_graph_from_binary_stream(self, binary_stream: BinaryIO) -> pd.DataFrame:
        logger.debug("Reading temp graph")
        df = pd.read_json(binary_stream, encoding=self._encoding)
        df.rename(columns=self._column_names_equal, inplace=True)
        logger.debug("Temp graph is read")
        return df
