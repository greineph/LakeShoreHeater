from lakeshore import Model372, Model372InputChannelSettings

# Variable Data, should be set before start

# ip address of the lakeshore module
IP_ADDRESS = ""

# Settings of heater
# channel of heater (1-16,A)
CHANNEL_HEATER = Model372.InputChannel.CONTROL
# auto range mode of heater (off, current)
AUTO_RANGE_MODE_HEATER = Model372.AutoRangeMode.CURRENT

# Settings of thermometer
# channel of thermometer (1-16,A)
CHANNEL_THERMOMETER = Model372.InputChannel.ONE
# auto range mode of thermometer (off, current)
AUTO_RANGE_MODE_THERMOMETER = Model372.AutoRangeMode.CURRENT
# sensor excitation mode of thermometer (voltage, current)
SENSOR_EXCITATION_MODE_THERMOMETER = Model372.SensorExcitationMode.VOLTAGE
# excitation range (voltage?) pf thermometer (?)
# TODO: clarify requirements for "Excitation Voltage"
EXCITATION_RANGE_THERMOMETER = None

