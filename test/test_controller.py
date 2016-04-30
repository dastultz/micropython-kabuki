import unittest

from kabuki.controller import FunctionInput, ValueInput, Controller, ValueOutput, FunctionOutput
from kabuki.operators import Operand


class TestController(unittest.TestCase):

    def test_end_to_end(self):
        global function_output_value

        controller = Controller()
        vi = CustomValueInput()
        fi = good_input_function
        op1 = controller.input(vi)
        op2 = controller.input(fi)

        cvo = CustomValueOutput()
        controller.output(op1, cvo)
        controller.output(op2, output_setter_function)

        self.assertEqual(0.0, op1.value, "should be initial value because update() hasn't been called yet")
        self.assertEqual(0.0, op2.value, "should be initial value because update() hasn't been called yet")
        self.assertEqual(None, function_output_value, "should be initial value because update() hasn't been called yet")
        self.assertEqual(None, cvo.value, "should be initial value because update() hasn't been called yet")

        controller.update()

        self.assertEqual(3.5, op1.value, "should be default value of CustomValueInput")
        self.assertEqual("yay!", op2.value, "should be value returned by good_input_function")
        self.assertEqual(3.5, cvo.value, "should be default value of CustomValueInput")
        self.assertEqual("yay!", function_output_value, "should be value returned by good_input_function")

    def test_bad_input(self):
        """ input supplier is not callable, does not have value property """
        controller = Controller()
        try:
            controller.input("Fred")
            self.fail("expected exception")
        except RuntimeError:
            pass

    def test_bad_output(self):
        """ output consumer is not callable, does not have value property """
        controller = Controller()
        try:
            controller.output(Operand(1.23), "Fred")
            self.fail("expected exception")
        except RuntimeError:
            pass


class CustomValueOutput:

    def __init__(self):
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class TestValueOutput(unittest.TestCase):

    def test_basic(self):
        cvo = CustomValueOutput()
        op = Operand("bogus")
        vo = ValueOutput(op, cvo)
        op.value = "Fred"
        self.assertEqual(None, cvo.value, "should be initial value because update() hasn't been called yet")
        vo.update()
        self.assertEqual("Fred", cvo.value, "should now have value from op")


function_output_value = None


def output_setter_function(value):
    global function_output_value
    function_output_value = value


class TestFunctionOutput(unittest.TestCase):

    def test_basic(self):
        global function_output_value
        function_output_value = 1
        op = Operand("bogus")
        fo = FunctionOutput(op, output_setter_function)
        op.value = 42
        self.assertEqual(1, function_output_value, "should have initial value because update() hasn't been called yet")
        fo.update()
        self.assertEqual(42, function_output_value, "should have value from op")


class CustomValueInput:

    @property
    def value(self):
        return 3.5


class TestValueInput(unittest.TestCase):

    def test_basic(self):
        vi = ValueInput(CustomValueInput())
        self.assertEqual(0.0, vi.value, "should have initial value because update() hasn't been called yet")
        vi.update()
        self.assertEqual(3.5, vi.value, "should be default value of CustomValueInput")

    def test_operable(self):
        vi = ValueInput(CustomValueInput())
        self.assertEqual(0.0, vi.value, "should have initial value because update() hasn't been called yet")
        vi.update()
        vi += 1.2
        self.assertEqual(4.7, vi.value, "should be default value of CustomValueInput + 1.2")


def bad_input_function():
    pass


def good_input_function():
    return "yay!"


class TestFunctionInput(unittest.TestCase):

    def test_return_value(self):
        fi = FunctionInput(good_input_function)
        fi.update()
        self.assertEqual("yay!", fi.value, "should be value returned by good_input_function")

    def test_operable(self):
        fi = FunctionInput(good_input_function)
        fi.update()
        fi += "dude"
        self.assertEqual("yay!dude", fi.value, "should be value returned by good_input_function + dude")

    def test_no_return_value(self):
        """ function does not return a value """
        fi = FunctionInput(bad_input_function)
        try:
            fi.update()
            self.fail("expected exception")
        except RuntimeError:
            pass


