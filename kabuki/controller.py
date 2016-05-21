from kabuki.operators import Operator
from kabuki.timing import Profiler

class Controller:
    """ This class is used to create and manage inputs and outputs"""

    def __init__(self):
        self._inputs = []
        self._outputs = []
        self._profiler = None

    def poll_input(self, supplier):
        """
        Registers an object to be polled with each loop.
        :param supplier: An object with a poll function.
        """
        self._inputs.append(supplier)

    def wire_output(self, operand, consumer):
        """
        Connect an operand to an output (consumer)
        :param operand: The last operand to connect to the output.
        :param consumer: A function that can receive a value or an object with a value
        property.
        """
        if callable(consumer):
            self._outputs.append(FunctionOutput(operand, consumer))
        elif hasattr(consumer, "consume"):
            f = getattr(consumer, "consume")
            if not callable(f):
                raise RuntimeError("consumer attribute \"consume\" is not callable")
            self._outputs.append(ValueOutput(operand, consumer))
        else:
            raise RuntimeError("output consumer must be callable or have a consume function")

    def update(self):
        """ Reset all cached values, recalculate and send to outputs. """
        for output in self._outputs:
            output.reset()

        # poll non-auto-calculating inputs
        for input in self._inputs:
            try:
                input.poll()
            except TypeError:
                raise RuntimeError("object passed to poll_input() must have a poll() function.")

        for output in self._outputs:
            output.update()

    def run(self):
        while True:
            self.update()
            if self._profiler:
                self._profiler.update()

    def enable_profiling(self):
        self._profiler = Profiler()


class ValueInput(Operator):
    """ Adapts an arbitrary input (value supplier) to an operand."""

    def __init__(self, value_supplier):
        super().__init__()
        self._value_supplier = value_supplier

    def _calculate_value(self):
        return self._value_supplier.value


class FunctionInput(Operator):
    """ Adapts an arbitrary input (function returning a value) to an operand."""

    def __init__(self, value_getter_function):
        super().__init__()
        self._value_getter_function = value_getter_function

    def _calculate_value(self):
        val = self._value_getter_function()
        if val is None:
            raise RuntimeError("input function must return a value")
        return val


class Output:

    def __init__(self, operand):
        self._operand = operand

    def reset(self):
        self._operand.reset()


class ValueOutput(Output):
    """ Adapts an operand to an arbitrary output (value consumer)."""

    def __init__(self, operand, value_consumer):
        super().__init__(operand)
        self._value_consumer = value_consumer

    def update(self):
        self._value_consumer.consume(self._operand.value)


class FunctionOutput(Output):
    """ Adapts an operand to an arbitrary output (function that accepts a value)."""

    def __init__(self, operand, value_setter_function):
        super().__init__(operand)
        self._value_setter_function = value_setter_function

    def update(self):
        self._value_setter_function(self._operand.value)