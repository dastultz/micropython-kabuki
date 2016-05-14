import unittest

from kabuki.controller import FunctionInput, ValueInput, Controller, ValueOutput, FunctionOutput, Output
from kabuki.operators import Operand, Operator
from test.test_operators import CalcCountingOperator


class TestController(unittest.TestCase):

    def test_end_to_end(self):
        global function_output_value

        controller = Controller()
        vi = CustomValueSupplier()
        fi = good_input_function
        op1 = controller.node_from_object(vi)
        op2 = controller.node_from_function(fi)

        cvo = CustomValueConsumer()
        controller.wire_output(op1, cvo)
        controller.wire_output(op2, output_setter_function)

        # operators calculate values right away
        self.assertEqual(3.5, op1.value, "should be default value of CustomValueInput")
        self.assertEqual("yay!", op2.value, "should be value returned by good_input_function")
        # outputs need call to update() first
        self.assertEqual(None, function_output_value, "should be initial value because update() hasn't been called yet")
        self.assertEqual(None, cvo.value, "should be initial value because update() hasn't been called yet")

        # we need to call update to move values to outputs
        controller.update()
        self.assertEqual(3.5, cvo.value, "should be default value of CustomValueInput")
        self.assertEqual("yay!", function_output_value, "should be value returned by good_input_function")

    def test_poll_input_not_callable(self):
        """ input supplier has poll property but not callable """
        controller = Controller()
        try:
            controller.poll_input(BadSupplierNotCallable())
            controller.update()
            self.fail("expected exception")
        except RuntimeError:
            pass

    def test_poll_input_no_poll(self):
        """ input supplier does not have poll property """
        controller = Controller()
        try:
            controller.poll_input(BadSupplierNotCallable())
            controller.update()
            self.fail("expected exception")
        except RuntimeError:
            pass

    def test_bad_output(self):
        """ output consumer is not callable, does not have value property """
        controller = Controller()
        try:
            controller.wire_output(Operand(1.23), "Fred")
            self.fail("expected exception")
        except RuntimeError:
            pass


class BadSupplierNoPoll:

    def __init__(self):
        self.monkey = True


class BadSupplierNotCallable:

    def __init__(self):
        self.poll = True


class CustomValueConsumer:

    def __init__(self):
        self.value = None

    def consume(self, value):
        self.value = value


class TestValueOutput(unittest.TestCase):

    def test_basic(self):
        cvc = CustomValueConsumer()
        op = Operand("bogus")
        vo = ValueOutput(op, cvc)
        op._value = "Fred"
        self.assertEqual(None, cvc.value, "should be initial value because update() hasn't been called yet")
        vo.update()
        self.assertEqual("Fred", cvc.value, "should now have value from op")


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
        op._value = 42
        self.assertEqual(1, function_output_value, "should have initial value because update() hasn't been called yet")
        fo.update()
        self.assertEqual(42, function_output_value, "should have value from op")


class CustomValueSupplier:

    @property
    def value(self):
        return 3.5


class TestValueInput(unittest.TestCase):

    def test_basic(self):
        vi = ValueInput(CustomValueSupplier())
        self.assertEqual(3.5, vi.value, "should be default value of CustomValueSupplier")

    def test_operable(self):
        vi = ValueInput(CustomValueSupplier())
        vi += 1.2
        self.assertEqual(4.7, vi.value, "should be default value of CustomValueSupplier + 1.2")


def bad_input_function():
    pass


def good_input_function():
    return "yay!"


class TestFunctionInput(unittest.TestCase):

    def test_return_value(self):
        fi = FunctionInput(good_input_function)
        self.assertEqual("yay!", fi.value, "should be value returned by good_input_function")

    def test_operable(self):
        fi = FunctionInput(good_input_function)
        fi += "dude"
        self.assertEqual("yay!dude", fi.value, "should be value returned by good_input_function + dude")

    def test_no_return_value(self):
        """ function does not return a value """
        fi = FunctionInput(bad_input_function)
        try:
            fi.value
            self.fail("expected exception")
        except RuntimeError:
            pass


class CustomPollableSupplier():

    def __init__(self):
        self.called = False

    def poll(self):
        self.called = True


class TestInputUpdate(unittest.TestCase):

    def test_simple(self):
        controller = Controller()
        a = CustomPollableSupplier()
        controller.poll_input(a)

        self.assertFalse(a.called)
        controller.update()
        self.assertTrue(a.called)


class TestCalcCaching(unittest.TestCase):

    def test_simple(self):
        controller = Controller()
        n1 = Operand(value=2)
        n2 = Operand(value=4)
        n3 = n1 + n2
        out = CustomValueConsumer()
        controller.wire_output(n3, out)
        controller.update()
        self.assertEqual(6, out.value)
        n1._value = 3
        self.assertEqual(6, out.value)
        controller.update()
        self.assertEqual(7, out.value)
