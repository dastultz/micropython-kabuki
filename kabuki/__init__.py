from kabuki.controller import Controller, FunctionInput, ValueInput
from kabuki.operators import Operand

""" Provide a default controller and façade methods. """

_default_controller = Controller()


def node_from_function(supplier):
    """
    Create a node with a value supplied by a function.
    :param supplier: A function that returns a value.
    :return: A node that can be operated on.
    """
    return FunctionInput(supplier)


def node_from_object(supplier):
    """ create a node with a value supplied from an object
    :param supplier: an object with a value property
    :return: a node that can be operated on
    """
    return ValueInput(supplier)


def node_from_value(value):
    """ create a node from a literal value
    :param value: a literal value
    :return: a node that can be operated on
    """
    return Operand(value=value)


def poll_input(supplier):
    _default_controller.poll_input(supplier)


def wire_output(operand, consumer):
    _default_controller.wire_output(operand, consumer)


def run():
    _default_controller.run()