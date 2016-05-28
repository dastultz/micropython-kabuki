class Slider:

    height = 75
    width = 20

    def __init__(self, label, min, max, x, y, applet, is_input = True):
        self._applet = applet
        self._label = label
        self._min = min
        self._max = max
        self._x = x
        self._y = y
        self._mouse_dragging = False
        self.value = self._min
        self._last_mouse_down = False
        self._is_input = is_input

    def service(self, mouse_down):
        if self._is_input:
            self._track_mouse(mouse_down)
        self._draw()

    def _track_mouse(self, mouse_down):
        if mouse_down \
                and self._last_mouse_down == False \
                and self._is_mouse_inside():
            self._mouse_dragging = True
        elif not mouse_down and self._last_mouse_down:
            self._mouse_dragging = False
        if self._mouse_dragging:
            my = self._applet.mouseY
            self.value = self._applet.map(my, self._y + self.height, self._y, self._min, self._max)
            self.value = self._applet.constrain(self.value, self._min, self._max)
        self._last_mouse_down = mouse_down

    def _is_mouse_inside(self):
        mx = self._applet.mouseX
        my = self._applet.mouseY
        if (self._x < mx < (self._x + self.width)) \
                and (self._y < my < (self._y + self.height)):
            return True
        else:
            return False

    def _draw(self):
        self._applet.fill(0)
        self._applet.stroke(204, 102, 0)
        self._applet.rect(self._x, self._y, self.width, self.height)
        h = self._applet.map(self.value, self._min, self._max, 0, self.height)
        h = self._applet.constrain(h, 0, self.height - 2)
        self._applet.fill(255)
        self._applet.stroke(255)
        self._applet.rect(self._x + 1, self.height - h + self._y - 1, self.width - 2, h)