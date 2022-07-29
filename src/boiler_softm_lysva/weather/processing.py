from typing import Union

import pandas as pd
from boiler.constants import column_names
from boiler.data_processing.beetween_filter_algorithm import AbstractTimestampFilterAlgorithm, \
    LeftClosedTimestampFilterAlgorithm
from boiler.data_processing.timestamp_interpolator_algorithm import AbstractTimestampInterpolationAlgorithm, \
    TimestampInterpolationAlgorithm
from boiler.data_processing.timestamp_round_algorithm import AbstractTimestampRoundAlgorithm, \
    CeilTimestampRoundAlgorithm
from boiler.data_processing.value_interpolation_algorithm import AbstractValueInterpolationAlgorithm, \
    LinearInsideValueInterpolationAlgorithm, LinearOutsideValueInterpolationAlgorithm
from boiler.weather.processing import AbstractWeatherProcessor
from dateutil import tz

from boiler_softm_lysva.constants.time_tick import TIME_TICK


class SoftMLysvaWeatherForecastProcessor(AbstractWeatherProcessor):

    def __init__(self,
                 timestamp_round_algorithm: AbstractTimestampRoundAlgorithm =
                 CeilTimestampRoundAlgorithm(round_step=TIME_TICK),
                 timestamp_interpolation_algorithm: AbstractTimestampInterpolationAlgorithm =
                 TimestampInterpolationAlgorithm(
                     CeilTimestampRoundAlgorithm(round_step=TIME_TICK),
                     TIME_TICK
                 ),
                 timestamp_filter_algorithm: AbstractTimestampFilterAlgorithm =
                 LeftClosedTimestampFilterAlgorithm(),
                 border_values_interpolation_algorithm: AbstractValueInterpolationAlgorithm =
                 LinearInsideValueInterpolationAlgorithm(),
                 internal_values_interpolation_algorithm: AbstractValueInterpolationAlgorithm =
                 LinearOutsideValueInterpolationAlgorithm()
                 ) -> None:
        self._columns_to_interpolate = [column_names.WEATHER_TEMP]
        self._timestamp_round_algorithm = timestamp_round_algorithm
        self._timestamp_interpolation_algorithm = timestamp_interpolation_algorithm
        self._timestamp_filter_algorithm = timestamp_filter_algorithm
        self._border_values_interpolation_algorithm = border_values_interpolation_algorithm
        self._internal_values_interpolation_algorithm = internal_values_interpolation_algorithm

    def process_weather_df(self,
                           weather_df: pd.DataFrame,
                           min_required_timestamp: Union[pd.Timestamp, None],
                           max_required_timestamp: Union[pd.Timestamp, None]
                           ) -> pd.DataFrame:
        min_required_timestamp = min_required_timestamp.tz_convert(tz.UTC)
        max_required_timestamp = max_required_timestamp.tz_convert(tz.UTC)

        weather_df = weather_df.copy()
        weather_df = self._convert_timestamp_to_utc(weather_df)
        weather_df = self._round_timestamp(weather_df)
        weather_df = self._drop_duplicates_by_timestamp(weather_df)
        weather_df = self._interpolate_timestamp(max_required_timestamp, min_required_timestamp, weather_df)
        weather_df = self._interpolate_values(weather_df)
        weather_df = self._filter_by_timestamp(max_required_timestamp, min_required_timestamp, weather_df)
        return weather_df

    # noinspection PyMethodMayBeStatic
    def _convert_timestamp_to_utc(self, weather_df: pd.DataFrame) -> pd.DataFrame:
        weather_df = weather_df.copy()
        weather_df[column_names.TIMESTAMP] = weather_df[column_names.TIMESTAMP].dt.tz_convert(tz.UTC)
        return weather_df

    def _round_timestamp(self,
                         weather_df: pd.DataFrame
                         ) -> pd.DataFrame:
        weather_df = weather_df.copy()
        weather_df[column_names.TIMESTAMP] = self._timestamp_round_algorithm.round_series(
            weather_df[column_names.TIMESTAMP]
        )
        return weather_df

    # noinspection PyMethodMayBeStatic
    def _drop_duplicates_by_timestamp(self,
                                      weather_df: pd.DataFrame
                                      ) -> pd.DataFrame:
        weather_df = weather_df.drop_duplicates(column_names.TIMESTAMP, keep="last")
        return weather_df

    def _interpolate_timestamp(self,
                               max_required_timestamp: Union[pd.Timestamp, None],
                               min_required_timestamp: Union[pd.Timestamp, None],
                               weather_df: pd.DataFrame
                               ) -> pd.DataFrame:
        weather_df = weather_df.copy()
        weather_df = self._timestamp_interpolation_algorithm.process_df(
            weather_df,
            min_required_timestamp,
            max_required_timestamp
        )
        return weather_df

    def _interpolate_values(self,
                            weather_df: pd.DataFrame
                            ) -> pd.DataFrame:
        weather_df = weather_df.copy()
        for column_name in self._columns_to_interpolate:
            weather_df[column_name] = self._border_values_interpolation_algorithm.interpolate_series(
                weather_df[column_name]
            )
            weather_df[column_name] = self._internal_values_interpolation_algorithm.interpolate_series(
                weather_df[column_name]
            )
        return weather_df

    def _filter_by_timestamp(self,
                             max_required_timestamp: Union[pd.Timestamp, None],
                             min_required_timestamp: Union[pd.Timestamp, None],
                             weather_df: pd.DataFrame
                             ) -> pd.DataFrame:
        weather_df = self._timestamp_filter_algorithm.filter_df_by_min_max_timestamp(
            weather_df,
            min_required_timestamp,
            max_required_timestamp
        )
        return weather_df
