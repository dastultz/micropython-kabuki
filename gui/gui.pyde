
import sys
sys.path.append("../../")

from kabuki.operators import Operand


from kabuki.controller import Controller
from controls import Slider

s1 = Slider("A", -5, 5, 10, 10, this)
s1.value = -5

s2 = Slider("B", -2, 2, 40, 10, this, is_input=False)

mouse_down = False

controller = Controller()
op1 = controller.input(s1)
op2 = op1 * 2
controller.output(op2, s2)

def setup():
    size(900, 120)


def draw():
    controller.update()
    background(51)
    s1.service(mouse_down)
    s2.service(mouse_down)


def mousePressed():
    global mouse_down
    mouse_down = True


def mouseReleased():
    global mouse_down
    mouse_down = False
