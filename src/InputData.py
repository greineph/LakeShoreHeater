from lakeshore import Model372, Model372InputChannelSettings

# Variable Data, should be set before start

# ip address of the lakeshore module
IP_ADDRESS = ""

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
RESISTANCE_RANGE_HEATER = Model372.MeasurementInputResistance.RANGE_2_OHMS


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
RESISTANCE_RANGE_THERMOMETER = Model372.MeasurementInputResistance.RANGE_2_OHMS

# Settings for filter
# turn filter on/off (True, False)
STATE_FILTER = True
# settle time of filter in seconds (1-200)
SETTLE_TIME_FILTER = 5
# specifies what percent of full scale reading limits the filtering function (1-80)
WINDOW_FILTER = 20

# TODO: sample rate

