from boiler.constants import column_names

BOILER_NEED_INTERPOLATE_COLUMNS = [
    column_names.FORWARD_PIPE_COOLANT_TEMP,
    column_names.BACKWARD_PIPE_COOLANT_TEMP,
    column_names.FORWARD_PIPE_COOLANT_PRESSURE,
    column_names.BACKWARD_PIPE_COOLANT_PRESSURE,
    column_names.FORWARD_PIPE_COOLANT_VOLUME,
    column_names.BACKWARD_PIPE_COOLANT_VOLUME
]

APARTMENT_HOUSE_NEED_INTERPOLATE_COLUMNS = [
    column_names.TIMESTAMP,
    column_names.FORWARD_PIPE_COOLANT_TEMP,
    column_names.BACKWARD_PIPE_COOLANT_TEMP,
]