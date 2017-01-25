import json

import pyb
from kabuki.operators import Operator, DictSourceOperator
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


class ThrottledIn:

    def __init__(self, delegate, milliseconds):
        self._delegate = delegate
        self._last_sample_time = 0
        self._threshold = milliseconds

    def poll(self):
        current = pyb.millis()
        elapsed = current - self._last_sample_time
        if elapsed >= self._threshold:
            self._delegate.poll()
            self._last_sample_time = current


class SerialIn:

    def __init__(self):
        self._serial = pyb.USB_VCP()
        self._dict = {}
        self._channel_definitions = []

    def poll(self):
        if self._serial.isconnected():
            lines = self._serial.readlines()
            for line in lines:
                if len(line) > 1:  # need more than just a new line character
                    line = line.decode()
                    if line.startswith("?"):
                        self._send_definitions()
                    else:
                        # each line assumed to be JSON of key value pairs
                        try:
                            self._dict.update(json.loads(line))
                        except:
                            print("ignoring bad JSON: %s" % line)

    def channel(self, label=None, default_value=None, min=None, max=None):
        key = str(len(self._channel_definitions))
        self._channel_definitions.append({"k": key, "l": label, "m": min, "M": max})
        return DictSourceOperator(key, self._dict, default_value=default_value)

    def _send_definitions(self):
        # copy the current value to the definition
        for definition in self._channel_definitions:
            definition["v"] = self._dict[definition["k"]]
        json_str = json.dumps(self._channel_definitions)
        print(json_str)
