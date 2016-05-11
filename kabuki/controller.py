from kabuki.operators import Operand


class Controller:
    """ This class is used to create and manage inputs and outputs"""

    def __init__(self):
        self._inputs = []
        self._outputs = []

    def input(self, supplier):
        """ Create and register an input.
        :param supplier: A function that returns a value, or an object with a value property,
            or an object with an update method
        :return: For true suppliers, an operand that can be operated on. You must call update()
            before the first value is available. For updatable objects, the original object.
        """
        if callable(supplier):
            operand = FunctionInput(supplier)
        elif hasattr(supplier, "value"):
            operand = ValueInput(supplier)
        elif hasattr(supplier, "update"):
            update_function = getattr(supplier, "update")
            if not callable(update_function):
                raise RuntimeError("input supplier \"update\" is not callable")
            operand = supplier # not sure this is really right, want to add to _inputs but maybe not return anything
        else:
            raise RuntimeError("input supplier must be callable or have a value property")
        self._inputs.append(operand)
        return operand

    def output(self, operand, consumer):
        """ Create and register an output.
        :param operand: The last operand to connect to the output.
        :param consumer: A function that can receive a value or an object with a value
        property. You must call update() for the first value to passed to the consumer.
        """
        if callable(consumer):
            self._outputs.append(FunctionOutput(operand, consumer))
        elif hasattr(consumer, "value"):
            self._outputs.append(ValueOutput(operand, consumer))
        else:
            raise RuntimeError("output consumer must be callable or have a value property")

    def update(self):
        """ Poll all inputs and propagate values to the outputs."""
        for input in self._inputs:
            input.update()

        for output in self._outputs:
            output.update()


class ValueInput(Operand):
    """ Adapts an arbitrary input (value supplier) to an operand."""

    def __init__(self, value_supplier):
        super().__init__()
        self._value_supplier = value_supplier

    def update(self):
        self.value = self._value_supplier.value


class FunctionInput(Operand):
    """ Adapts and arbitrary input (function returning a value) to an operand."""

    def __init__(self, value_getter_function):
        super().__init__()
        self._value_getter_function = value_getter_function

    def update(self):
        val = self._value_getter_function()
        if val is None:
            raise RuntimeError("input function must return a value")
        self.value = val


class ValueOutput:
    """ Adapts an operand to an arbitrary output (value consumer)."""

    def __init__(self, operand, value_consumer):
        self._operand = operand
        self._value_consumer = value_consumer

    def update(self):
        self._value_consumer.value = self._operand.value


class FunctionOutput:
    """ Adapts an operand to an arbitrary output (function that accepts a value)."""

    def __init__(self, operand, value_setter_function):
        self._operand = operand
        self._value_setter_function = value_setter_function

    def update(self):
        self._value_setter_function(self._operand.value)