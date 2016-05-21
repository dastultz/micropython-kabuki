from kabuki import timing


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

    def __gt__(self, other):
        return GreaterThan(self, other)

    def __lt__(self, other):
        return LessThan(self, other)

    def __ge__(self, other):
        return GreaterOrEqual(self, other)

    def __le__(self, other):
        return LessOrEqual(self, other)

    def filter_above(self, other):
        return FilterAbove(self, other)

    def filter_below(self, other):
        return FilterBelow(self, other)

    def constrain(self, lower, upper):
        return Constrain(self, lower, upper)

    def map(self, in_start, in_stop, out_start, out_stop, constrain=True):
        op = Map(self, in_start, in_stop, out_start, out_stop)
        if constrain:
            return op.constrain(out_start, out_stop)
        else:
            return op

    def retain_between(self, lower, upper):
        return RetainBetween(self, lower, upper)

    def reduce_noise(self, band):
        return ReduceNoise(self, band)

    def throttle(self, milliseconds):
        return Throttle(self, milliseconds)


class Operator(Operable):
    """ Performs "lazy" or deferred calculations on objects.
        Calculations are cached between calls to reset(). """

    def __init__(self):
        super().__init__()
        self._cached_value = None

    @property
    def value(self):
        if self._cached_value is None:
            self._cached_value = self._calculate_value()
        return self._cached_value

    def reset(self):
        self._cached_value = None

    def _calculate_value(self):
        pass


class Operand(Operator):
    """ A wrapper around a literal value that can be operated on. """

    def __init__(self, value=0.0):
        super().__init__()
        self._value = value

    def _calculate_value(self):
        return self._value


class SingleArgumentOperator(Operator):

    def __init__(self, operand):
        super().__init__()
        self._first_operand = self._wrap_if_needed(operand)

    def _wrap_if_needed(self, operand):
        if not hasattr(operand, "value"):
            operand = Operand(value=operand)
        return operand

    def reset(self):
        super().reset()
        self._first_operand.reset()


class DoubleArgumentOperator(SingleArgumentOperator):

    def __init__(self, first_operand, second_operand):
        super().__init__(first_operand)
        self._second_operand = self._wrap_if_needed(second_operand)

    def reset(self):
        super().reset()
        self._second_operand.reset()


class TripleArgumentOperator(DoubleArgumentOperator):

    def __init__(self, first_operand, second_operand, third_operand):
        super().__init__(first_operand, second_operand)
        self._third_operand = self._wrap_if_needed(third_operand)

    def reset(self):
        super().reset()
        self._third_operand.reset()


class QuadrupleArgumentOperator(TripleArgumentOperator):

    def __init__(self, first_operand, second_operand, third_operand, fourth_operand):
        super().__init__(first_operand, second_operand, third_operand)
        self._fourth_operand = self._wrap_if_needed(fourth_operand)

    def reset(self):
        super().reset()
        self._fourth_operand.reset()


class QuintupleArgumentOperator(QuadrupleArgumentOperator):

    def __init__(self, first_operand, second_operand, third_operand, fourth_operand, fifth_operand):
        super().__init__(first_operand, second_operand, third_operand, fourth_operand)
        self._fifth_operand = self._wrap_if_needed(fifth_operand)

    def reset(self):
        super().reset()
        self._fifth_operand.reset()


class Add(DoubleArgumentOperator):

    def _calculate_value(self):
        return self._first_operand.value + self._second_operand.value


class Sub(DoubleArgumentOperator):

    def _calculate_value(self):
        return self._first_operand.value - self._second_operand.value


class Neg(SingleArgumentOperator):

    def _calculate_value(self):
        value = self._first_operand.value
        if value is True:
            return False
        elif value is False:
            return True
        else:
            return -value


class Abs(SingleArgumentOperator):

    def _calculate_value(self):
        return abs(self._first_operand.value)


class Div(DoubleArgumentOperator):

    def _calculate_value(self):
        # todo: should we make this a "safe" divide (by zero)?
        return self._first_operand.value / self._second_operand.value


class Mul(DoubleArgumentOperator):

    def _calculate_value(self):
        return self._first_operand.value * self._second_operand.value


class GreaterThan(DoubleArgumentOperator):

    def _calculate_value(self):
        return self._first_operand.value > self._second_operand.value


class LessThan(DoubleArgumentOperator):
    def _calculate_value(self):
        return self._first_operand.value < self._second_operand.value


class GreaterOrEqual(DoubleArgumentOperator):
    def _calculate_value(self):
        return self._first_operand.value >= self._second_operand.value


class LessOrEqual(DoubleArgumentOperator):
    def _calculate_value(self):
        return self._first_operand.value <= self._second_operand.value


class FilterAbove(DoubleArgumentOperator):

    def _calculate_value(self):
        value = self._first_operand.value
        limit = self._second_operand.value
        if value < limit:
            return value
        else:
            return 0


class FilterBelow(DoubleArgumentOperator):

    def _calculate_value(self):
        value = self._first_operand.value
        limit = self._second_operand.value
        if value > limit:
            return value
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


class Constrain(TripleArgumentOperator):

    def _calculate_value(self):
        val = self._first_operand.value
        bound_1 = self._second_operand.value
        bound_2 = self._third_operand.value
        upper = bound_1 if bound_1 > bound_2 else bound_2
        lower = bound_2 if bound_2 < bound_1 else bound_1
        return min(upper, max(lower, val))


class Map(QuintupleArgumentOperator):

    def _calculate_value(self):
        val = self._first_operand.value
        in_start = self._second_operand.value
        in_stop = self._third_operand.value
        out_start = self._fourth_operand.value
        out_stop = self._fifth_operand.value

        return _map(val, in_start, in_stop, out_start, out_stop)


def _map(value, in_start, in_stop, out_start, out_stop):
    return out_start + (out_stop - out_start) * ((value - in_start) / (in_stop - in_start))


class ReduceNoise(DoubleArgumentOperator):

    def __init__(self, first_operand, second_operand):
        super().__init__(first_operand, second_operand)
        self._last_trend_direction = True  # True for "up"
        self._last_trend_value = 0 # the last value that was in the trend direction

    def _calculate_value(self):
        band = self._second_operand.value
        current_value = self._first_operand.value
        diff = current_value - self._last_trend_value
        current_direction = True if diff >= 0 else False

        if current_direction != self._last_trend_direction:
            if abs(diff) >= band:
                self._last_trend_direction = current_direction
                self._last_trend_value = current_value
                value = current_value
            else:
                value = self._last_trend_value
        else:
            self._last_trend_value = current_value
            value = current_value

        return value


class Throttle(SingleArgumentOperator):

    def __init__(self, first_operand, milliseconds):
        super().__init__(first_operand)
        self._last_sample_time = 0
        self._threshold = milliseconds

    def _calculate_value(self):
        self._last_sample_time = timing.millis()
        return self._first_operand.value

    def reset(self):
        current = timing.millis()
        elapsed = current - self._last_sample_time
        if elapsed >= self._threshold:
            super().reset()


class Cycler(DoubleArgumentOperator):

    def __init__(self, first_operand, second_operand, initial_position = 0):
        super().__init__(first_operand, second_operand)
        self._position = initial_position

    def _calculate_value(self):
        length = self._first_operand.value
        delta = self._second_operand.value
        self._position += delta
        # todo: consider wrap around vs stop
        # todo: how could we do a ping/pong? delta is external
        if self._position > length:
            self._position = 0
        elif self._position < 0:
            self._position = length
        return self._position

    def channel(self, keys):
        return Channel(self, self._first_operand, keys)


class Channel(DoubleArgumentOperator):

    def __init__(self, first_operand, second_operand, keys):
        super().__init__(first_operand, second_operand)
        try:
            self._xlist = []
            self._ylist = []
            for x, y in keys:
                x = self._wrap_if_needed(x)
                y = self._wrap_if_needed(y)
                self._xlist.append(x)
                self._ylist.append(y)
            self._key_count = len(keys)
        except:
            raise RuntimeError("error parsing keys, must be list of 2 Tuples")
        if self._key_count == 0:
            raise RuntimeError("keys must have at least one key!")

    def _calculate_value(self):
        # find keys where position between two x's, interpolate
        position = self._first_operand.value
        cycler_length = self._second_operand.value
        left_x_count = 0 # number of keys to the left of current position
        # assumes x values are sorted low to high
        for v in self._xlist:
            if v.value <= position:
                left_x_count += 1

        # a little repetition here, but looking for performance
        if 0 < left_x_count < self._key_count:
            left_x_index = left_x_count - 1
            right_x_index = left_x_count
            left_x = self._xlist[left_x_index].value
            right_x = self._xlist[right_x_index].value
            left_y = self._ylist[left_x_index].value
            right_y = self._ylist[right_x_index].value
        elif left_x_count == self._key_count:
            # pos is to right of all keys, flip first after last
            left_x_index = -1
            right_x_index = 0
            left_x = self._xlist[left_x_index].value
            right_x = self._xlist[right_x_index].value + cycler_length
            left_y = self._ylist[left_x_index].value
            right_y = self._ylist[right_x_index].value
        else:  # left_x_count == 0:
            # pos is to left of all keys, flip last before first
            left_x_index = -1
            right_x_index = 0
            left_x = self._xlist[left_x_index].value - cycler_length
            right_x = self._xlist[right_x_index].value
            left_y = self._ylist[left_x_index].value
            right_y = self._ylist[right_x_index].value

        return _map(position, left_x, right_x, left_y, right_y)
