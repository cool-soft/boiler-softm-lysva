from typing import BinaryIO

import pandas as pd
from boiler.temp_graph.io.abstract_sync_temp_graph_reader import AbstractSyncTempGraphReader

import boiler_softm_lysva.constants.converting_parameters
from boiler_softm_lysva.logging import logger


class SoftMLysvaSyncTempGraphOnlineReader(AbstractSyncTempGraphReader):

    def __init__(self,
                 encoding: str = "utf-8"
                 ) -> None:
        self._encoding = encoding
        self._column_names_equal = boiler_softm_lysva.constants.converting_parameters.TEMP_GRAPH_COLUMN_NAMES_EQUALS

        logger.debug(
            f"Creating instance:"
            f"encoding: {encoding}"
        )

    def read_temp_graph_from_binary_stream(self,
                                           binary_stream: BinaryIO
                                           ) -> pd.DataFrame:
        logger.debug("Reading temp graph")
        df = pd.read_json(binary_stream, encoding=self._encoding)
        df = self._rename_columns(df)
        logger.debug("Temp graph is read")
        return df

    def _rename_columns(self,
                        df: pd.DataFrame
                        ) -> pd.DataFrame:
        logger.debug("Renaming columns")
        df = df.rename(columns=self._column_names_equal).copy()
        return df
