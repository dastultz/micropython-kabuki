import pyb
from kabuki.operators import Operator
from ppm_decoder import Decoder


class UserSwitchIn(Operator):

    def __init__(self):
        super().__init__()
        self._sw = pyb.Switch()

    def _calculate_value(self):
        return self._sw()


class AccelIn:

    def __init__(self):
        self._accel = pyb.Accel()
        self._accel.write(0x07, self._accel.read(0x07) & 0b11111110)  # place in stand by mode to write registers
        self._accel.write(0x08, self._accel.read(0x08) & 0b11111000)  # 120 samples/sec
        self._accel.write(0x07, self._accel.read(0x07) | 0b00000001)  # return to active mode
        self._values = {"x": 0, "y": 0, "z": 0}

    def poll(self):
        x, y, z = self._accel.filtered_xyz()
        self._values["x"] = x
        self._values["y"] = y
        self._values["z"] = z

    def x(self):
        return AxisOperator(self._values, "x")

    def y(self):
        return AxisOperator(self._values, "y")

    def z(self):
        return AxisOperator(self._values, "x")


class AxisOperator(Operator):

    def __init__(self, all_axes, axis):
        super().__init__()
        self._all_axes = all_axes
        self._axis = axis

    def _calculate_value(self):
        return self._all_axes[self._axis]


class PpmIn:

    def __init__(self, pin: str):
        self._decoder = Decoder(pin)

    def channel(self, channel: int):
        return ChannelOperator(channel, self._decoder)


class ChannelOperator(Operator):

    def __init__(self, channel: int, ppm_in):
        super().__init__()
        self._channel = channel
        self._ppm_in = ppm_in

    def _calculate_value(self):
        return self._ppm_in.get_channel_value(self._channel)