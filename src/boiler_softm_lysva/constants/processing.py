from boiler.constants import column_names

BOILER_NEED_INTERPOLATE_COLUMNS = [
    column_names.FORWARD_TEMP,
    column_names.BACKWARD_TEMP,
    column_names.FORWARD_PRESSURE,
    column_names.BACKWARD_PRESSURE,
    column_names.FORWARD_VOLUME,
    column_names.BACKWARD_VOLUME
]

APARTMENT_HOUSE_NEED_INTERPOLATE_COLUMNS = [
    column_names.TIMESTAMP,
    column_names.FORWARD_TEMP,
    column_names.BACKWARD_TEMP,
]
