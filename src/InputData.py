from lakeshore import Model372, Model372InputChannelSettings

# Variable Data, should be set before start

# ip address of the lakeshore module
IP_ADDRESS = "192.168.0.12"

# Settings of heater
# channel of heater (1-16,A)
CHANNEL_HEATER = Model372.InputChannel.ONE
# sensor excitation mode of heater (current, voltage)
SENSOR_EXCITATION_MODE_HEATER = Model372.SensorExcitationMode.CURRENT
# excitation range of heater (Channel 1-16: MeasurementInputRange, A: ControlInputCurrentRange)
EXCITATION_RANGE_HEATER = Model372.MeasurementInputCurrentRange.RANGE_1_MICRO_AMP
# auto range mode of heater (off, current)
AUTO_RANGE_MODE_HEATER = Model372.AutoRangeMode.CURRENT
# shunt current source of heater (True, False)
CURRENT_SOURCE_SHUNTED_HEATER = False
# units for sensor of heater (kelvin, ohms)
UNITS_HEATER = Model372.InputSensorUnits.OHMS
# measurement input resistance range of heater (MeasurementInputResistance, None)
RESISTANCE_RANGE_HEATER = Model372.MeasurementInputResistance.RANGE_63_POINT_2_KIL_OHMS
# list of wanted readings ["kelvin", "resistance", "power", "quadrature"(not in Control channel)] for heater
WANTED_READINGS_HEATER = ["kelvin", "resistance", "power", "quadrature"]


# Settings of thermometer
# channel of thermometer (1-16,A)
CHANNEL_THERMOMETER = Model372.InputChannel.CONTROL
# sensor excitation mode of thermometer (voltage, current)
SENSOR_EXCITATION_MODE_THERMOMETER = Model372.SensorExcitationMode.CURRENT
# excitation range of thermometer (Channel 1-16: MeasurementInputRange, A: ControlInputCurrentRange)
EXCITATION_RANGE_THERMOMETER = Model372.ControlInputCurrentRange.RANGE_1_NANO_AMP
# auto range mode of thermometer (off, current)
AUTO_RANGE_MODE_THERMOMETER = Model372.AutoRangeMode.CURRENT
# shunt current source of thermometer (True, False)
CURRENT_SOURCE_SHUNTED_THERMOMETER = False
# units for sensor of thermometer (kelvin, ohms)
UNITS_THERMOMETER = Model372.InputSensorUnits.OHMS
# measurement input resistance range of thermometer (MeasurementInputResistance, None)
RESISTANCE_RANGE_THERMOMETER = Model372.MeasurementInputResistance.RANGE_63_POINT_2_KIL_OHMS
# list of wanted readings ["kelvin", "resistance", "power", "quadrature"(not in Control channel)] for thermometer
WANTED_READINGS_THERMOMETER = ["kelvin", "resistance", "power"]


# Settings for MPV
# whether to use mpv client
MPV_ENABLED = True
# list of wanted readings ["field", "temperature"] for mpv client
WANTED_READINGS_MPV = ["field", "temperature"]
# TODO: do more settings

# Settings for filter
# turn filter on/off (True, False)
STATE_FILTER = True
# settle time of filter in seconds (1-200)
SETTLE_TIME_FILTER = 5
# specifies what percent of full scale reading limits the filtering function (1-80)
WINDOW_FILTER = 10

# Settings for data logging
# Seconds between logged datapoints
SAMPLE_RATE = 2


def range_text_converter(text: str):
    text = text.replace("RANGE_", "")
    text = text.replace("_POINT_", ".")
    text = text.replace("MEGA_", "M")
    text = text.replace("KIL_", "K")
    text = text.replace("MILLI_", "m")
    text = text.replace("MICRO_", "µ")
    text = text.replace("NANO_", "n")
    text = text.replace("PICO_", "p")
    text = text.replace("AMPS", "A")
    text = text.replace("AMP", "A")
    text = text.replace("OHMS", "O")
    text = text.replace("_", "\t")
    return text
