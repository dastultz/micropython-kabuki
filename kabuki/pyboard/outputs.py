import pyb


# LED output
class LedOut:

    def __init__(self, led_number):
        self._led = pyb.LED(led_number)

    @property
    def value(self):
        return None

    @value.setter
    def value(self, value):
        if value == 0:
            self._led.off()
        else:
            self._led.on()


# Servo output
class ServoOut:

    def __init__(self, servo_number):
        self._servo = pyb.Servo(servo_number)

    @property
    def value(self):
        return None

    @value.setter
    def value(self, value):
        # todo: should we consrain angle for safety?
        self._servo.angle(value)