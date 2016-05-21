import pyb

"""
This module exists merely to encapsulate the dependency on pyb.
Could inject other hardware platforms here.
"""


def millis():
    return pyb.millis()


class Profiler:

    def __init__(self):
        self._last_time = 0
        self._count = 0

    def update(self):
        current = pyb.millis()
        if current - self._last_time >= 1000:
            print(self._count)
            self._last_time = current
            self._count = 0
        self._count += 1
