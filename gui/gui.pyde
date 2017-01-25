

from comm import Comm

mouse_down = False
comm = Comm()


def setup():
    size(350, 500)
    textFont(createFont("AmericanTypewriter", 12))


def draw():
    background(51)
    comm.service(mouse_down, this)


def mousePressed():
    global mouse_down
    mouse_down = True


def mouseReleased():
    global mouse_down
    mouse_down = False