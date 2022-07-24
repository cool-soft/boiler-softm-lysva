from typing import Optional

import pandas as pd
import requests
from boiler.data_processing.beetween_filter_algorithm \
    import AbstractTimestampFilterAlgorithm, LeftClosedTimestampFilterAlgorithm
from boiler.weather.io.abstract_sync_weather_loader import AbstractSyncWeatherLoader
from boiler.weather.io.abstract_sync_weather_reader import AbstractSyncWeatherReader

from boiler_softm_lysva.constants import api_constants
from boiler_softm_lysva.logging import logger


class SoftMLysvaSyncWeatherForecastOnlineLoader(AbstractSyncWeatherLoader):

    def __init__(self,
                 reader: AbstractSyncWeatherReader,
                 timestamp_filter_algorithm: AbstractTimestampFilterAlgorithm =
                 LeftClosedTimestampFilterAlgorithm(),
                 api_base: str = api_constants.API_BASE,
                 http_proxy: Optional[str] = None,
                 https_proxy: Optional[str] = None
                 ) -> None:
        self._weather_reader = reader
        self._api_base = api_base
        self._timestamp_filter_algorithm = timestamp_filter_algorithm
        self._proxies = {}
        if http_proxy is not None:
            self._proxies.update({"http": http_proxy})
        if https_proxy is not None:
            self._proxies.update({"https": https_proxy})
        logger.debug(
            f"Creating instance: "
            f"reader: {self._weather_reader} "
            f"api_base: {self._api_base} "
            f"timestamp_filter_algorithm: {self._timestamp_filter_algorithm} "
            f"http_proxy: {http_proxy} "
        )

    def load_weather(self,
                     start_datetime: Optional[pd.Timestamp] = None,
                     end_datetime: Optional[pd.Timestamp] = None
                     ) -> pd.DataFrame:
        logger.debug(f"Requested weather forecast from {start_datetime} to {end_datetime}")
        url = f"{self._api_base}/JSON"
        # noinspection SpellCheckingInspection
        params = {
            "method": "getPrognozT"
        }
        with requests.get(url=url, params=params, proxies=self._proxies, stream=True) as response:
            logger.debug(f"Weather forecast is loaded. Status code is {response.status_code}")
            weather_df = self._weather_reader.read_weather_from_binary_stream(response.raw)
        weather_df = self._timestamp_filter_algorithm.filter_df_by_min_max_timestamp(
            weather_df,
            start_datetime,
            end_datetime
        )
        logger.debug(f"Gathered {len(weather_df)} weather forecast items")
        return weather_df
