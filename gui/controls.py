
text_width = 125
height = 20
width = 75

class Slider:

    def __init__(self, key, label, min, max, value, x, y, applet, comm, is_input=True):
        self._applet = applet
        self._key = key
        self._label = label
        self._min = min
        self._max = max
        self._x = x
        self._y = y
        self._mouse_dragging = False
        self._value = value
        self._last_mouse_down = False
        self._comm = comm
        self._is_input = is_input

    def service(self, mouse_down):
        if self._is_input:
            self._track_mouse(mouse_down)
        self._draw()

    def _track_mouse(self, mouse_down):
        if (mouse_down
                and self._last_mouse_down is False
                and self._is_mouse_inside()):
            self._mouse_dragging = True
        elif not mouse_down and self._last_mouse_down:
            self._mouse_dragging = False
        if self._mouse_dragging:
            mx = self._applet.mouseX
            x = self._x + text_width
            self._value = self._applet.map(mx, x, x + width, self._min, self._max)
            self._value = self._applet.constrain(self._value, self._min, self._max)
            self._comm.send_value(self._key, self._value)
        self._last_mouse_down = mouse_down

    def _is_mouse_inside(self):
        mx = self._applet.mouseX
        my = self._applet.mouseY
        x = self._x + text_width
        if ((x < mx < (x + width))
                and (self._y < my < (self._y + height))):
            return True
        else:
            return False

    def _draw(self):
        self._applet.textAlign(self._applet.LEFT, self._applet.TOP);
        self._applet.fill(255)
        self._applet.text(self._label, self._x, self._y + 5)
        formatted_value = "{:.3f}".format(self._value)
        self._applet.text(formatted_value, self._x + text_width + width + 5, self._y + 5)

        self._applet.fill(0)
        self._applet.stroke(204, 102, 0)

        x = self._x + text_width

        # border
        self._applet.rect(x, self._y, width, height)

        # value bar
        w = self._applet.map(self._value, self._min, self._max, 0, width)
        w = self._applet.constrain(w, 0, width - 2)
        self._applet.fill(255)
        self._applet.stroke(255)
        self._applet.rect(x + 1, self._y + 1, w, height - 2)


def slider_from_dict(definition, x, y, applet, self):
    key = definition["k"]
    label = definition["l"]
    min = definition["m"]
    max = definition["M"]
    value = definition["v"]
    return Slider(key, label, min, max, value, x, y, applet, self)