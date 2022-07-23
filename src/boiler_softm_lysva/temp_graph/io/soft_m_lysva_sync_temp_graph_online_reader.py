from typing import BinaryIO

import pandas as pd
from boiler.temp_graph.io.abstract_sync_temp_graph_reader import AbstractSyncTempGraphReader

from boiler_softm_lysva.constants import converting_parameters
from boiler_softm_lysva.logging import logger


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
