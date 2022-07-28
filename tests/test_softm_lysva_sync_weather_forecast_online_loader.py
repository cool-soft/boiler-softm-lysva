import pytest
from boiler.constants import column_names
# noinspection PyProtectedMember
from pandas.api.types import is_numeric_dtype, is_datetime64tz_dtype

from boiler_softm_lysva.weather.io import SoftMLysvaSyncWeatherForecastOnlineLoader, \
    SoftMLysvaSyncWeatherForecastOnlineReader


class TestSoftMLysvaSyncWeatherForecastOnlineLoader:

    @pytest.fixture
    def reader(self):
        return SoftMLysvaSyncWeatherForecastOnlineReader()

    @pytest.fixture
    def loader(self, reader, is_need_proxy, proxy_address):
        http_proxy = None
        https_proxy = None
        if is_need_proxy:
            http_proxy = proxy_address
            https_proxy = proxy_address
        loader = SoftMLysvaSyncWeatherForecastOnlineLoader(
            reader=reader,
            http_proxy=http_proxy,
            https_proxy=https_proxy
        )
        return loader

    def test_loader(self, loader):
        weather_forecast_df = loader.load_weather()

        assert not weather_forecast_df.empty

        assert column_names.TIMESTAMP in weather_forecast_df.columns
        assert column_names.WEATHER_TEMP in weather_forecast_df.columns

        assert is_datetime64tz_dtype(weather_forecast_df[column_names.TIMESTAMP])
        assert is_numeric_dtype(weather_forecast_df[column_names.WEATHER_TEMP])
