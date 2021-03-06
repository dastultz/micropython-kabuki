from kabuki import timing


class Operable:
    """ Provides for "object-oriented math". Calculations are deferred until requested."""

    def add(self, node):
        return Add(self, node)

    def sub(self, node):
        return Sub(self, node)

    def mul(self, node):
        return Mul(self, node)

    def div(self, node):
        return Div(self, node)

    def neg(self):
        return Neg(self)

    def abs(self):
        return Abs(self)

    def filter_above(self, node):
        return FilterAbove(self, node)

    def filter_below(self, node):
        return FilterBelow(self, node)

    def filter_between(self, lower_node, upper_node):
        return FilterBetween(self, lower_node, upper_node)

    def constrain(self, lower_node, upper_node):
        return Constrain(self, lower_node, upper_node)

    def map(self, in_start_node, in_stop_node, out_start_node, out_stop_node, constrain=True):
        op = Map(self, in_start_node, in_stop_node, out_start_node, out_stop_node)
        if constrain:
            return op.constrain(out_start_node, out_stop_node)
        else:
            return op

    def retain_between(self, lower_node, upper_node):
        return RetainBetween(self, lower_node, upper_node)

    def reduce_noise(self, band_node):
        return ReduceNoise(self, band_node)

    def throttle(self, milliseconds):
        return Throttle(self, milliseconds)

    def debug(self, label):
        return Debug(self, label)

    def swap(self, a, b, sustain_time = None):
        return Swap(self, a, b, sustain_time=sustain_time)


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
        denominator = self._second_operand.value
        if denominator == 0:
            return 0
        return self._first_operand.value / denominator


class Mul(DoubleArgumentOperator):

    def _calculate_value(self):
        return self._first_operand.value * self._second_operand.value

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


class FilterBetween(TripleArgumentOperator):

    def _calculate_value(self):
        val = self._first_operand.value
        lower = self._second_operand.value
        upper = self._third_operand.value
        if lower <= val <= upper:
            return 0
        else:
            return val


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

    def __init__(self, value_node, band):
        super().__init__(value_node, band)
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

    def __init__(self, value_node, milliseconds):
        super().__init__(value_node)
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


class Debug(SingleArgumentOperator):

    def __init__(self, node, label):
        super().__init__(node)
        self._label = label

    def _calculate_value(self):
        # todo: be nice to print all values on one line and add new line per loop
        value = self._first_operand.value
        print("%s : %s" %(self._label, value))
        return value


# todo: needs a reset concept, after sustain_time reached, resets to "a" for some time (same as sustain?)
class Swap(TripleArgumentOperator):

    def __init__(self, control, a, b, sustain_time = None):
        super().__init__(control, a, b)
        self._sustain_time = None if sustain_time is None else int(sustain_time * 1000)
        self._release_time = None
        self._last_main = True  # taking the main path, "a"

    def _calculate_value(self):
        control = self._first_operand
        a = self._second_operand
        b = self._third_operand
        v = a.value

        main = (control.value is None
            or control.value == 0
            or not control)

        if self._sustain_time is not None:
            # we've just switched to the alternate path, start timing
            if self._last_main and not main:
                self._release_time = timing.millis() + self._sustain_time
            # check if time has expired
            if (self._release_time is not None
                    and timing.millis() >= self._release_time):
                self._release_time = None

        if self._release_time is not None or not main:
            v = b.value

        self._last_main = main
        return v


class Cycler(DoubleArgumentOperator):

    def __init__(self, length_node, delta_node, initial_position = 0):
        super().__init__(length_node, delta_node)
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

    def __init__(self, position_node, length_node, keys):
        super().__init__(position_node, length_node)
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

    def reset(self):
            for v in self._xlist:
                v.reset()
            for v in self._ylist:
                v.reset()
            super().reset()


class DictSourceOperator(SingleArgumentOperator):

    # op is an Operator with a value that is a dictionary
    def __init__(self, key, op, default_value=None):
        super().__init__(op)
        self._key = key
        self._op = self._first_operand
        self._default_value = default_value

    def _calculate_value(self):
        values = self._op.value
        try:
            value = values[self._key]
        except KeyError:
            values[self._key] = self._default_value
            value = self._default_value
        return value
