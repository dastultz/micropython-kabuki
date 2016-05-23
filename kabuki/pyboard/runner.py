import kabuki, sys
import pyb


class Loader:

    def __init__(self):
        self._reload_queued = True
        self.queue_reload()

    def poll(self):
        if self._reload_queued:
            self._reload()
            self._reload_queued = False

    def queue_reload(self):
        self._reload_queued = True

    def _reload(self):
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
    kabuki.run()


if __name__ == "__main__":
    run()