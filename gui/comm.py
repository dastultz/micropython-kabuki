import json

import controls

add_library('serial')
from processing.serial import Serial

class Comm:

    def __init__(self):
        self._init = False
        self._sent_request = False
        self._controls = []
        self._values = {}
        self._serial = None #  todo: need a close hook

    def service(self, mouse_down, applet):
        if self._init:
            for control in self._controls:
                control.service(mouse_down)
            while self._serial.available() > 0:
                line = self._serial.readStringUntil(10)
                if line is not None:
                    print("> %s" %line.strip())
        else:
            self._try_to_build(applet)

    def _try_to_build(self, applet):
        if self._serial is not None:
            if self._sent_request:

                json_str = self._serial.readStringUntil(10)

                if json_str is not None:
                    try:
                        definitions = json.loads(json_str.decode())
                        self._build_control(definitions, applet)
                        self._init = True
                    except ValueError:
                        print(json_str.strip())
            else:
                print("Requesting definitions")
                self._serial.write("?\n".encode())
                self._sent_request = True
        else:
            self._try_to_establish_serial()

    def _build_control(self, definitions, applet):
        x = 10
        y = 5
        for definition in definitions:
            control = controls.slider_from_dict(definition, x, y, applet, self)
            self._controls.append(control)
            y += controls.height

    def _try_to_establish_serial(self):
        try:
            print(Serial.list())
            self._serial = Serial(this, "/dev/tty.usbmodem1412", 9600)  # max rate?
            print("*** established serial connection")
        except Exception as exc:
            print("*** error attempting to connect to Pyboard : %s" %exc)
            self._serial = None

    def send_value(self, key, value):
        try:
            old = self._values[key]
        except KeyError:
            old = None
        if old != value:
            d = {key: value}
            json_str = json.dumps(d).encode()
            print("sending %s" % json_str)
            self._serial.write(json_str)
            self._serial.write("\n".encode())
        self._values[key] = value

    def send(com, value):
        com.write(json.dumps(value).encode())
        com.write("\n".encode())
        for line in com.readlines():
            if len(line) > 1:
                print("> %s" % line.decode())
