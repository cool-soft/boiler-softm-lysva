import pytest
from boiler.constants import column_names
# noinspection PyProtectedMember
from pandas.api.types import is_numeric_dtype

from boiler_softm_lysva.temp_graph.io import SoftMLysvaSyncTempGraphOnlineLoader, SoftMLysvaSyncTempGraphOnlineReader


class TestSoftMLysvaSyncTempGraphOnlineLoader:

    @pytest.fixture
    def reader(self):
        return SoftMLysvaSyncTempGraphOnlineReader()

    @pytest.fixture
    def loader(self, reader, is_need_proxy, proxy_address):
        http_proxy = None
        https_proxy = None
        if is_need_proxy:
            http_proxy = proxy_address
            https_proxy = proxy_address
        loader = SoftMLysvaSyncTempGraphOnlineLoader(
            reader=reader,
            http_proxy=http_proxy,
            https_proxy=https_proxy
        )
        return loader

    def test_loader(self, loader):
        temp_graph_df = loader.load_temp_graph()

        assert not temp_graph_df.empty

        assert column_names.WEATHER_TEMP in temp_graph_df.columns
        assert column_names.FORWARD_TEMP in temp_graph_df.columns
        assert column_names.BACKWARD_TEMP in temp_graph_df.columns

        assert is_numeric_dtype(temp_graph_df[column_names.WEATHER_TEMP])
        assert is_numeric_dtype(temp_graph_df[column_names.FORWARD_TEMP])
        assert is_numeric_dtype(temp_graph_df[column_names.BACKWARD_TEMP])
