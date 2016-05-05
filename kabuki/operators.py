

class Operable:
    """ Provides for "object-oriented math". Calculations are deferred until requested."""

    def __add__(self, other):
        return Add(self, other)

    def __radd__(self, other):
        return Add(self, other)

    def __sub__(self, other):
        return Sub(self, other)

    def __rsub__(self, other):
        return Sub(other, self)

    def __mul__(self, other):
        return Mul(self, other)

    def __rmul__(self, other):
        return Mul(self, other)

    def __truediv__(self, other):
        return Div(self, other)

    def __rtruediv__(self, other):
        return Div(other, self)

    def __neg__(self):
        return Neg(self)

    def __abs__(self):
        return Abs(self)

    def filter_above(self, other):
        return FilterAbove(self, other)

    def filter_below(self, other):
        return FilterBelow(self, other)

    def retain_between(self, lower, upper):
        return RetainBetween(self, lower, upper)

    # other ideas

    # upper limit (max), reduce greater values to that of second operand < and <=
    # lower limit (min), raise lower values to that of second operand > and >=

    # buffer/smooth/average

    # mid band, for noisy input required to be on one side of a threshold
    # for return, require greater movement, maybe this is a feature of filter/retain

    # https://docs.python.org/3/library/operator.html


class Operand(Operable):
    """ A wrapper around a value that can be operated on."""

    def __init__(self, value=0.0):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Operator(Operable):
    """ Performs "lazy" or deferred calculations on objects."""

    @property
    def value(self):
        return self._calculate_value()

    def _calculate_value(self):
        pass


class SingleArgumentOperator(Operator):

    def __init__(self, operand):
        super().__init__()
        self._operand = operand


class DoubleArgumentOperator(Operator):

    def __init__(self, first_operand, second_operand):
        super().__init__()
        self._first_operand = self._wrap_if_needed(first_operand)
        self._second_operand = self._wrap_if_needed(second_operand)

    def _wrap_if_needed(self, operand):
        if not hasattr(operand, "value"):
            operand = Operand(value=operand)
        return operand


class TripleArgumentOperator(DoubleArgumentOperator):

    def __init__(self, first_operand, second_operand, third_operand):
        super().__init__(first_operand, second_operand)
        self._third_operand = self._wrap_if_needed(third_operand)


class Add(DoubleArgumentOperator):

    def _calculate_value(self):
        return self._first_operand.value + self._second_operand.value


class Sub(DoubleArgumentOperator):

    def _calculate_value(self):
        return self._first_operand.value - self._second_operand.value


class Neg(SingleArgumentOperator):

    def _calculate_value(self):
        return (-self._operand.value)


class Abs(SingleArgumentOperator):

    def _calculate_value(self):
        return abs(self._operand.value)


class Div(DoubleArgumentOperator):

    def _calculate_value(self):
        # todo: should we make this a "safe" divide (by zero)?
        return self._first_operand.value / self._second_operand.value


class Mul(DoubleArgumentOperator):

    def _calculate_value(self):
        return self._first_operand.value * self._second_operand.value


class FilterAbove(DoubleArgumentOperator):

    def _calculate_value(self):
        if self._first_operand.value <= self._second_operand.value:
            return self._first_operand.value
        else:
            return 0


class FilterBelow(DoubleArgumentOperator):

    def _calculate_value(self):
        if self._first_operand.value >= self._second_operand.value:
            return self._first_operand.value
        else:
            return 0


class RetainBetween(TripleArgumentOperator):

    def _calculate_value(self):
        val = self._first_operand.value
        lower = self._second_operand.value
        upper = self._third_operand.value
        if lower <= val <= upper:
            return val
        else:
            return 0