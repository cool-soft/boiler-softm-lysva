import io
from datetime import tzinfo
from typing import Optional, BinaryIO

import pandas as pd
import requests
from boiler.constants import column_names
from boiler.data_processing.beetween_filter_algorithm import AbstractTimestampFilterAlgorithm, \
    LeftClosedTimestampFilterAlgorithm
from boiler.weather.io.abstract_sync_weather_loader import AbstractSyncWeatherLoader
from boiler.weather.io.abstract_sync_weather_reader import AbstractSyncWeatherReader

from boiler_softm_lysva.constants import api_constants, converting_parameters, column_names as soft_m_column_names
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


class SoftMLysvaSyncWeatherForecastOnlineReader(AbstractSyncWeatherReader):

    def __init__(self,
                 encoding: str = "utf-8",
                 weather_data_timezone: tzinfo = None
                 ) -> None:
        self._weather_data_timezone = weather_data_timezone
        self._encoding = encoding
        self._column_names_equals = converting_parameters.WEATHER_INFO_COLUMN_EQUALS

        logger.debug(
            f"Creating instance:"
            f"weather_data_timezone: {self._weather_data_timezone}"
            f"encoding: {self._encoding}"
        )

    def read_weather_from_binary_stream(self, binary_stream: BinaryIO) -> pd.DataFrame:
        logger.debug("Parsing weather")
        with io.TextIOWrapper(binary_stream, encoding=self._encoding) as text_stream:
            df = pd.read_json(text_stream, convert_dates=False)
        df.rename(columns=self._column_names_equals, inplace=True)
        self._convert_date_and_time_to_timestamp(df)
        logger.debug("Weather is parsed")
        return df

    def _convert_date_and_time_to_timestamp(self, df: pd.DataFrame) -> None:
        logger.debug("Converting dates and time to timestamp")

        dates_as_str = df[soft_m_column_names.WEATHER_DATE]
        time_as_str = df[soft_m_column_names.WEATHER_TIME]
        datetime_as_str = dates_as_str.str.cat(time_as_str, sep=" ")
        timestamp = pd.to_datetime(datetime_as_str)
        timestamp = timestamp.dt.tz_localize(self._weather_data_timezone)

        df[column_names.TIMESTAMP] = timestamp
        del df[soft_m_column_names.WEATHER_TIME]
        del df[soft_m_column_names.WEATHER_DATE]
