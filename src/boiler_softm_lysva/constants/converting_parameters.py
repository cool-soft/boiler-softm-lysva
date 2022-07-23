from boiler.constants import column_names, circuit_types

from boiler_softm_lysva.constants import column_names as lysva_column_names
from boiler_softm_lysva.constants.circuit_ids import HOT_WATER_CIRCUIT, HEATING_CIRCUIT

BOILER_AVAILABLE_COLUMNS = [
    column_names.TIMESTAMP,
    column_names.FORWARD_PIPE_COOLANT_TEMP,
    column_names.BACKWARD_PIPE_COOLANT_TEMP,
    column_names.FORWARD_PIPE_COOLANT_PRESSURE,
    column_names.BACKWARD_PIPE_COOLANT_PRESSURE,
    column_names.FORWARD_PIPE_COOLANT_VOLUME,
    column_names.BACKWARD_PIPE_COOLANT_VOLUME
]
BOILER_FLOAT_COLUMNS = [
    column_names.FORWARD_PIPE_COOLANT_TEMP,
    column_names.BACKWARD_PIPE_COOLANT_TEMP,
    column_names.FORWARD_PIPE_COOLANT_PRESSURE,
    column_names.BACKWARD_PIPE_COOLANT_PRESSURE,
    column_names.FORWARD_PIPE_COOLANT_VOLUME,
    column_names.BACKWARD_PIPE_COOLANT_VOLUME
]
APARTMENT_HOUSE_AVAILABLE_COLUMNS = [
    column_names.TIMESTAMP,
    column_names.FORWARD_PIPE_COOLANT_TEMP,
    column_names.BACKWARD_PIPE_COOLANT_TEMP,
]
APARTMENT_HOUSE_FLOAT_COLUMNS = [
    column_names.FORWARD_PIPE_COOLANT_TEMP,
    column_names.BACKWARD_PIPE_COOLANT_TEMP,
]
TEMP_GRAPH_COLUMN_NAMES_EQUALS = {
    lysva_column_names.TEMP_GRAPH_WEATHER_TEMP: column_names.WEATHER_TEMP,
    lysva_column_names.TEMP_GRAPH_TEMP_AT_IN: column_names.FORWARD_PIPE_COOLANT_TEMP,
    lysva_column_names.LYSVA_TEMP_GRAPH_TEMP_AT_OUT: column_names.BACKWARD_PIPE_COOLANT_TEMP
}
WEATHER_INFO_COLUMN_EQUALS = {
    lysva_column_names.WEATHER_TEMP: column_names.WEATHER_TEMP
}
HEATING_OBJ_COLUMN_NAMES_EQUALS = {
    lysva_column_names.HEATING_SYSTEM_TIMESTAMP: column_names.TIMESTAMP,
    lysva_column_names.HEATING_SYSTEM_FORWARD_PIPE_COOLANT_TEMP: column_names.FORWARD_PIPE_COOLANT_TEMP,
    lysva_column_names.HEATING_SYSTEM_BACKWARD_PIPE_COOLANT_TEMP: column_names.BACKWARD_PIPE_COOLANT_TEMP,
    lysva_column_names.HEATING_SYSTEM_FORWARD_PIPE_COOLANT_VOLUME: column_names.FORWARD_PIPE_COOLANT_VOLUME,
    lysva_column_names.HEATING_SYSTEM_BACKWARD_PIPE_COOLANT_VOLUME: column_names.BACKWARD_PIPE_COOLANT_VOLUME,
    lysva_column_names.HEATING_SYSTEM_FORWARD_PIPE_COOLANT_PRESSURE: column_names.FORWARD_PIPE_COOLANT_PRESSURE,
    lysva_column_names.HEATING_SYSTEM_BACKWARD_PIPE_COOLANT_PRESSURE: column_names.BACKWARD_PIPE_COOLANT_PRESSURE
}
HEATING_OBJ_TIMESTAMP_PARSING_PATTERNS = (
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s(?P<hours>\d{2}):(?P<minutes>\d{2}).{7}",
    r"(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})\s(?P<hours>\d{1,2}):(?P<minutes>\d{2})"
)
CIRCUIT_EQUALS = {
    HOT_WATER_CIRCUIT: circuit_types.HOT_WATER,
    HEATING_CIRCUIT: circuit_types.HEATING
}
