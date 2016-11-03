import kabuki, sys
import pyb
from kabuki.operators import Cycler
from kabuki.pyboard.outputs import LedOut


class Loader:

    def __init__(self):
        self._reload_queued = True
        self.queue_reload()

    def poll(self):
        if self._reload_queued:
            self._reload_queued = False
            self._reload()

    def queue_reload(self):
        self._reload_queued = True

    def _reload(self):
        for i in range(1, 4):
            pyb.LED(i).off()
        green = pyb.LED(2)
        green.on()
        pyb.delay(500)
        green.off()
        kabuki._default_controller.clear()
        mod_name = "nodes"
        if mod_name in sys.modules:
            del sys.modules[mod_name]
        import nodes  # executes module loading in node definitions
        kabuki.poll_input(self)


def run():
    loader = Loader()
    kabuki.poll_input(loader)
    sw = pyb.Switch()
    sw.callback(loader.queue_reload)
    while True:
        try:
            kabuki.run()
        except Exception as exc:
            sys.print_exception(exc)
            _install_police_lights(loader)


def _install_police_lights(loader):
    kabuki._default_controller.clear()
    kabuki.poll_input(loader)

    cycler = Cycler(5, 0.02)

    red_keys = [(0, 0), (1, 1), (2, 0), (4, 0)]
    blue_keys = [(0, 0), (2, 0), (3, 1), (4, 0)]

    red_led_blinker = cycler.channel(red_keys)
    blue_led_blinker = cycler.channel(blue_keys)

    kabuki.wire_output(red_led_blinker, LedOut(1))
    kabuki.wire_output(blue_led_blinker, LedOut(4))

if __name__ == "__main__":
    run()