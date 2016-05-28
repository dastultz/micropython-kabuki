import unittest

from kabuki.operators import *


class TestAdd(unittest.TestCase):

    def test_simple(self):
        n1 = Operand(value=1.5)
        n2 = Operand(value=3.75)

        op = Add(n1, n2)
        self.assertEqual(5.25, op.value)

        n1._value = 1.75
        self.assertEqual(5.25, op.value) # cached
        op.reset()
        self.assertEqual(5.5, op.value)

    def test_compound(self):
        n1 = Operand(value=1.5)
        n2 = Operand(value=3.75)
        n3 = Operand(value=0.125)

        op1 = Add(n1, n2)
        op2 = Add(op1, n3)
        self.assertEqual(5.375, op2.value)

    def test_non_number(self):
        n1 = Operand("hello ")
        n2 = Operand("world")

        op = n1 + n2
        self.assertEqual("hello world", op.value)

    def test_symbolic(self):
        n1 = Operand(1.25)
        n2 = Operand(2.5)
        n3 = Operand(0.25)

        op = n1 + n2 + n3
        self.assertEqual(4.0, op.value)

    def test_literal(self):
        n1 = Operand(value=5)

        n2 = n1 + 2
        self.assertEqual(n2.value, 7)

        n3 = 3 + n1
        self.assertEqual(n3.value, 8)


class TestNeg(unittest.TestCase):

    def test_simple(self):
        n = Operand(value=1.5)

        op = Neg(n)
        self.assertEqual(-1.5, op.value)

        n._value = -1.7
        self.assertEqual(-1.5, op.value) # cached
        op.reset()
        self.assertEqual(1.7, op.value)

    def test_compound(self):
        n = Operand(value=1.5)

        op1 = Neg(n)
        op2 = Neg(op1)
        self.assertEqual(1.5, op2.value)

    def test_symbolic(self):
        n = Operand(1.25)

        op = (-n)
        self.assertEqual(-1.25, op.value)

    def test_true(self):
        n = Operand(value=True)

        op = (-n)
        self.assertEqual(False, op.value)

    def test_false(self):
        n = Operand(value=False)

        op = (-n)
        self.assertEqual(True, op.value)


class TestSub(unittest.TestCase):

    def test_simple(self):
        n1 = Operand(value=1.5)
        n2 = Operand(value=0.25)

        op = Sub(n1, n2)
        self.assertEqual(1.25, op.value)

        n1._value = 1.75
        self.assertEqual(1.25, op.value) # cached
        op.reset()
        self.assertEqual(1.5, op.value)

    def test_compound(self):
        n1 = Operand(value=1.5)
        n2 = Operand(value=0.25)
        n3 = Operand(value=-0.5)

        op1 = Sub(n1, n2)
        op2 = Sub(op1, n3)
        self.assertEqual(1.75, op2.value)

    def test_symbolic(self):
        n1 = Operand(1.25)
        n2 = Operand(0.375)
        n3 = Operand(-0.125)

        op = n1 - n2 - n3
        self.assertEqual(1.0, op.value)

    def test_literal(self):
        n1 = Operand(value=5)

        n2 = n1 - 2
        self.assertEqual(n2.value, 3)

        n3 = 3 - n1
        self.assertEqual(n3.value, -2)


class TestAbs(unittest.TestCase):

    def test_simple(self):
        n = Operand(value=1.5)

        op = Abs(n)
        self.assertEqual(1.5, op.value)

        n = Operand(value=-1.6)

        op = Abs(n)
        self.assertEqual(1.6, op.value)

        n._value = -1.7
        self.assertEqual(1.6, op.value) # cached
        op.reset()
        self.assertEqual(1.7, op.value)

    def test_compound(self):
        n = Operand(value=-1.5)

        op1 = Abs(n)
        op2 = Abs(op1)
        self.assertEqual(1.5, op2.value)

    def test_symbolic(self):
        n1 = Operand(1.25)
        n2 = Operand(0.375)
        n3 = Operand(-0.125)

        op = n1 - n2 - abs(n3)
        self.assertEqual(0.75, op.value)


class TestDiv(unittest.TestCase):

    def test_simple(self):
        n1 = Operand(value=6.2)
        n2 = Operand(value=3.1)

        op = Div(n1, n2)
        self.assertEqual(2.0, op.value)

        n1._value = 6.3
        self.assertEqual(2.0, op.value) # cached
        op.reset()
        self.assertAlmostEqual(2.03, op.value, 2)

    def test_compound(self):
        n1 = Operand(value=12.4)
        n2 = Operand(value=2.0)
        n3 = Operand(value=3.1)

        op1 = Div(n1, n2)
        op2 = Div(op1, n3)
        self.assertEqual(2.0, op2.value)

    def test_symbolic(self):
        n1 = Operand(value=12.4)
        n2 = Operand(value=2.0)
        n3 = Operand(value=3.1)

        op = n1 / n2 / n3
        self.assertEqual(2.0, op.value)

    def test_literal(self):
        n1 = Operand(value=14)

        n2 = n1 / 2
        self.assertEqual(n2.value, 7)

        n3 = 28 / n1
        self.assertEqual(n3.value, 2)


class TestMul(unittest.TestCase):

    def test_simple(self):
        n1 = Operand(value=6.2)
        n2 = Operand(value=3.1)

        op = Mul(n1, n2)
        self.assertAlmostEqual(19.22, op.value, 2)

        n1._value = 6.3
        self.assertAlmostEqual(19.22, op.value, 2) # cached
        op.reset()
        self.assertAlmostEqual(19.53, op.value, 2)

    def test_compound(self):
        n1 = Operand(value=12.4)
        n2 = Operand(value=2.0)
        n3 = Operand(value=3.1)

        op1 = Mul(n1, n2)
        op2 = Mul(op1, n3)

        self.assertAlmostEqual(76.88, op2.value, 2)

    def test_symbolic(self):
        n1 = Operand(value=12.4)
        n2 = Operand(value=2.0)
        n3 = Operand(value=3.1)

        op = n1 * n2 * n3
        self.assertAlmostEqual(76.88, op.value, 2)

    def test_literal(self):
        n1 = Operand(value=5)

        n2 = n1 * 2
        self.assertEqual(n2.value, 10)

        n3 = 3 * n1
        self.assertEqual(n3.value, 15)


class TestGreaterThan(unittest.TestCase):

    def test_all(self):
        n1 = Operand(value=3)
        n2 = Operand(value=7)
        self.assertFalse((n1 > n2).value)

        n1 = Operand(value=7)
        n2 = Operand(value=3)
        self.assertTrue((n1 > n2).value)

        n1 = Operand(value=3)
        n2 = Operand(value=3)
        self.assertFalse((n1 > n2).value)


class TestLessThan(unittest.TestCase):

    def test_all(self):
        n1 = Operand(value=3)
        n2 = Operand(value=7)
        self.assertTrue((n1 < n2).value)

        n1 = Operand(value=7)
        n2 = Operand(value=3)
        self.assertFalse((n1 < n2).value)

        n1 = Operand(value=3)
        n2 = Operand(value=3)
        self.assertFalse((n1 < n2).value)


class TestGreaterOrEqual(unittest.TestCase):

    def test_all(self):
        n1 = Operand(value=3)
        n2 = Operand(value=7)
        self.assertFalse((n1 >= n2).value)

        n1 = Operand(value=7)
        n2 = Operand(value=3)
        self.assertTrue((n1 >= n2).value)

        n1 = Operand(value=3)
        n2 = Operand(value=3)
        self.assertTrue((n1 >= n2).value)


class TestLessOrEqual(unittest.TestCase):

    def test_all(self):
        n1 = Operand(value=3)
        n2 = Operand(value=7)
        self.assertTrue((n1 <= n2).value)

        n1 = Operand(value=7)
        n2 = Operand(value=3)
        self.assertFalse((n1 <= n2).value)

        n1 = Operand(value=3)
        n2 = Operand(value=3)
        self.assertTrue((n1 <= n2).value)


class TestFilterAbove(unittest.TestCase):

    def test_below(self):
        n1 = Operand(value=3)
        n2 = Operand(value=7)
        self.assertEqual(3, n1.filter_above(n2).value)

    def test_above(self):
        n1 = Operand(value=7)
        n2 = Operand(value=3)
        self.assertEqual(0, n1.filter_above(n2).value)

    def test_equal(self):
        n1 = Operand(value=3)
        n2 = Operand(value=3)
        self.assertEqual(0, n1.filter_above(n2).value)


class TestFilterBelow(unittest.TestCase):

    def test_above(self):
        n1 = Operand(value=7)
        n2 = Operand(value=3)

        self.assertEqual(7, n1.filter_below(n2).value)

    def test_below(self):
        n1 = Operand(value=3)
        n2 = Operand(value=7)
        self.assertEqual(0, n1.filter_below(n2).value)

    def test_equal(self):
        n1 = Operand(value=3)
        n2 = Operand(value=3)
        self.assertEqual(0, n1.filter_below(n2).value)


class TestFilterBetween(unittest.TestCase):

    def test_between(self):
        n1 = Operand(value=3)
        n2 = Operand(value=2)
        n3 = Operand(value=4)
        self.assertEqual(0, n1.filter_between(n2, n3).value)

    def test_below(self):
        n1 = Operand(value=2)
        n2 = Operand(value=3)
        n3 = Operand(value=5)
        self.assertEqual(2, n1.filter_between(n2, n3).value)

    def test_above(self):
        n1 = Operand(value=7)
        n2 = Operand(value=3)
        n3 = Operand(value=5)
        self.assertEqual(7, n1.filter_between(n2, n3).value)

    def test_equal_to_lower(self):
        n1 = Operand(value=3)
        n2 = Operand(value=3)
        n3 = Operand(value=5)
        self.assertEqual(0, n1.filter_between(n2, n3).value)

    def test_equal_to_upper(self):
        n1 = Operand(value=5)
        n2 = Operand(value=3)
        n3 = Operand(value=5)
        self.assertEqual(0, n1.filter_between(n2, n3).value)

    def test_wrap(self):
        n1 = Operand(value=3)

        self.assertEqual(0, n1.filter_between(2, 4).value)
        self.assertEqual(3, n1.filter_between(5, 7).value)
        self.assertEqual(3, n1.filter_between(0, 2).value)
        
        
class TestRetainBetween(unittest.TestCase):

    def test_between(self):
        n1 = Operand(value=3)
        n2 = Operand(value=2)
        n3 = Operand(value=4)
        self.assertEqual(3, n1.retain_between(n2, n3).value)

    def test_below(self):
        n1 = Operand(value=2)
        n2 = Operand(value=3)
        n3 = Operand(value=5)
        self.assertEqual(0, n1.retain_between(n2, n3).value)

    def test_above(self):
        n1 = Operand(value=7)
        n2 = Operand(value=3)
        n3 = Operand(value=5)
        self.assertEqual(0, n1.retain_between(n2, n3).value)

    def test_equal_to_lower(self):
        n1 = Operand(value=3)
        n2 = Operand(value=3)
        n3 = Operand(value=5)
        self.assertEqual(3, n1.retain_between(n2, n3).value)

    def test_equal_to_upper(self):
        n1 = Operand(value=5)
        n2 = Operand(value=3)
        n3 = Operand(value=5)
        self.assertEqual(5, n1.retain_between(n2, n3).value)

    def test_wrap(self):
        n1 = Operand(value=3)

        self.assertEqual(3, n1.retain_between(2, 4).value)
        self.assertEqual(0, n1.retain_between(5, 7).value)
        self.assertEqual(0, n1.retain_between(0, 2).value)


class TestConstrain(unittest.TestCase):

    def test_between(self):
        n1 = Operand(value=3)
        n2 = Operand(value=2)
        n3 = Operand(value=4)
        self.assertEqual(3, n1.constrain(n2, n3).value)

    def test_below(self):
        n1 = Operand(value=2)
        n2 = Operand(value=3)
        n3 = Operand(value=5)
        self.assertEqual(3, n1.constrain(n2, n3).value)

    def test_above(self):
        n1 = Operand(value=7)
        n2 = Operand(value=3)
        n3 = Operand(value=5)
        self.assertEqual(5, n1.constrain(n2, n3).value)

    def test_equal_to_lower(self):
        n1 = Operand(value=3)
        n2 = Operand(value=3)
        n3 = Operand(value=5)
        self.assertEqual(3, n1.constrain(n2, n3).value)

    def test_equal_to_upper(self):
        n1 = Operand(value=5)
        n2 = Operand(value=3)
        n3 = Operand(value=5)
        self.assertEqual(5, n1.constrain(n2, n3).value)

    def test_between_reversed(self):
        n1 = Operand(value=3)
        n2 = Operand(value=4)
        n3 = Operand(value=2)
        self.assertEqual(3, n1.constrain(n2, n3).value)

    def test_below_reversed(self):
        n1 = Operand(value=2)
        n2 = Operand(value=5)
        n3 = Operand(value=3)
        self.assertEqual(3, n1.constrain(n2, n3).value)

    def test_above_reversed(self):
        n1 = Operand(value=7)
        n2 = Operand(value=5)
        n3 = Operand(value=3)
        self.assertEqual(5, n1.constrain(n2, n3).value)

    def test_wrap(self):
        n1 = Operand(value=3)

        self.assertEqual(3, n1.constrain(2, 4).value)
        self.assertEqual(5, n1.constrain(5, 7).value)
        self.assertEqual(2, n1.constrain(0, 2).value)


class TestMap(unittest.TestCase):

    def test_simple_forward(self):
        n1 = Operand(value=2)
        n2 = Operand(value=0)
        n3 = Operand(value=10)
        n4 = Operand(value=0)
        n5 = Operand(value=100)
        self.assertEqual(20, n1.map(n2, n3, n4, n5).value)

    def test_simple_reverse(self):
        n1 = Operand(value=2)
        n2 = Operand(value=0)
        n3 = Operand(value=10)
        n4 = Operand(value=100)
        n5 = Operand(value=0)
        self.assertEqual(80, n1.map(n2, n3, n4, n5).value)

    def test_simple_above_constrained(self):
        n1 = Operand(value=22)
        n2 = Operand(value=10)
        n3 = Operand(value=20)
        n4 = Operand(value=20)
        n5 = Operand(value=100)
        self.assertEqual(100, n1.map(n2, n3, n4, n5).value)

    def test_simple_below_constrained(self):
        n1 = Operand(value=8)
        n2 = Operand(value=10)
        n3 = Operand(value=20)
        n4 = Operand(value=20)
        n5 = Operand(value=100)
        self.assertEqual(20, n1.map(n2, n3, n4, n5).value)

    def test_simple_above_unconstrained(self):
        n1 = Operand(value=22)
        n2 = Operand(value=10)
        n3 = Operand(value=20)
        n4 = Operand(value=20)
        n5 = Operand(value=100)
        self.assertEqual(116, n1.map(n2, n3, n4, n5, constrain=False).value)

    def test_simple_below_unconstrained(self):
        n1 = Operand(value=8)
        n2 = Operand(value=10)
        n3 = Operand(value=20)
        n4 = Operand(value=20)
        n5 = Operand(value=100)
        self.assertEqual(4, n1.map(n2, n3, n4, n5, constrain=False).value)

    def test_wrap(self):
        n1 = Operand(value=0.8)
        self.assertEqual(1360, n1.map(0, 1, 800, 1500).value)


class TestReduceNoise(unittest.TestCase):

    def test_start_to_up(self):
        n = Operand(value=7)
        op = n.reduce_noise(3)
        self.assertEqual(7, op.value)
        n._value = 9
        self.assertEqual(7, op.value) # cached
        op.reset()
        self.assertEqual(9, op.value)
        n._value = 7
        op.reset()
        self.assertEqual(9, op.value)
        n._value = 8
        op.reset()
        self.assertEqual(9, op.value)
        n._value = 10
        op.reset()
        self.assertEqual(10, op.value)
        n._value = 8
        op.reset()
        self.assertEqual(10, op.value)
        n._value = 7
        op.reset()
        self.assertEqual(7, op.value)
        n._value = 6
        op.reset()
        self.assertEqual(6, op.value)
        n._value = 8
        op.reset()
        self.assertEqual(6, op.value)
        n._value = 7
        op.reset()
        self.assertEqual(6, op.value)
        n._value = 5
        op.reset()
        self.assertEqual(5, op.value)
        n._value = 6
        op.reset()
        self.assertEqual(5, op.value)
        n._value = 10
        op.reset()
        self.assertEqual(10, op.value)

    def test_start_to_down(self):
        n = Operand(value=-3)
        op = n.reduce_noise(3)
        self.assertEqual(-3, op.value)
        n._value = -5
        op.reset()
        self.assertEqual(-5, op.value)
        n._value = -4
        op.reset()
        self.assertEqual(-5, op.value)
        n._value = -3
        op.reset()
        self.assertEqual(-5, op.value)
        n._value = -6
        op.reset()
        self.assertEqual(-6, op.value)
        n._value = -7
        op.reset()
        self.assertEqual(-7, op.value)
        n._value = -6
        op.reset()
        self.assertEqual(-7, op.value)
        n._value = -3
        op.reset()
        self.assertEqual(-3, op.value)


class TestIntegration(unittest.TestCase):

    def test_precedence(self):
        n1 = Operand(value=1)
        n2 = Operand(value=2)
        n3 = Operand(value=3)
        n4 = Operand(value=4)

        op = n1 + n2 / n3 + n4 * n2
        self.assertAlmostEqual(9.666, op.value, 2)

        op = (n1 + n2) / (n3 + n4) * n2
        self.assertAlmostEqual(0.857, op.value, 2)


class CalcCountingOperator(Operator):

    def __init__(self):
        super().__init__()
        self.count = 0

    def reset(self):
        super().reset()
        self.count = 0

    def _calculate_value(self):
        self.count += 1
        return 1


class TestCacheValue(unittest.TestCase):

    def test_calc(self):
        op = CalcCountingOperator()
        self.assertEqual(0, op.count)
        v = op.value
        self.assertEqual(1, op.count)
        v = op.value
        self.assertEqual(1, op.count)
        op.reset()
        self.assertEqual(0, op.count)
        v = op.value
        self.assertEqual(1, op.count)
        v = op.value
        self.assertEqual(1, op.count)

    def test_reset(self):
        n1 = Operand(value=10)
        n2 = Operand(value=20)
        n3 = Operand(value=30)
        n4 = Operand(value=40)
        n5 = Operand(value=50)

        op = MultiOperandAddOperator(n1, n2, n3, n4, n5)
        self.assertEqual(150, op.value)
        n1._value = 11
        self.assertEqual(150, op.value)
        op.reset()
        self.assertEqual(151, op.value)
        n2._value = 21
        self.assertEqual(151, op.value)
        op.reset()
        self.assertEqual(152, op.value)
        n3._value = 31
        self.assertEqual(152, op.value)
        op.reset()
        self.assertEqual(153, op.value)
        n4._value = 41
        self.assertEqual(153, op.value)
        op.reset()
        self.assertEqual(154, op.value)
        n5._value = 51
        self.assertEqual(154, op.value)
        op.reset()
        self.assertEqual(155, op.value)


class MultiOperandAddOperator(QuintupleArgumentOperator):
    """ This operator should always extend the operator with the most arguments.
    The purpose is to test that eaxh *ArgumentOperator class handles caching and reset.
    """

    def _calculate_value(self):
        n1 = self._first_operand.value
        n2 = self._second_operand.value
        n3 = self._third_operand.value
        n4 = self._fourth_operand.value
        n5 = self._fifth_operand.value

        return n1 + n2 + n3 + n4 + n5


class TestCycler(unittest.TestCase):

    def test_position_up(self):
        length = 10
        delta = 2
        cycler = Cycler(length, delta)
        self.assertEqual(2, cycler.value)
        cycler.reset()
        self.assertEqual(4, cycler.value)
        cycler.reset()
        self.assertEqual(6, cycler.value)
        cycler.reset()
        self.assertEqual(8, cycler.value)
        cycler.reset()
        self.assertEqual(10, cycler.value)
        cycler.reset()
        self.assertEqual(0, cycler.value)
        cycler.reset()

    def test_position_down(self):
        length = 10
        delta = -2
        cycler = Cycler(length, delta, initial_position=6)
        self.assertEqual(4, cycler.value)
        cycler.reset()
        self.assertEqual(2, cycler.value)
        cycler.reset()
        self.assertEqual(0, cycler.value)
        cycler.reset()
        self.assertEqual(10, cycler.value)


class TestChannel(unittest.TestCase):

    def test_middle(self):
        length = 10
        delta = 1
        cycler = Cycler(length, delta, initial_position=3)
        self.assertEqual(4, cycler.value)
        keys = [(2, 3), (6, 2), (9, 5)]
        channel = cycler.channel(keys)
        self.assertEqual(2.5, channel.value)

    def test_left(self):
        length = 10
        delta = 1
        cycler = Cycler(length, delta, initial_position=0)
        self.assertEqual(1, cycler.value)
        keys = [(3, 3), (6, 2), (9, 5)]
        channel = cycler.channel(keys)
        # (-1, 5), (3, 3) = 2/4 * 2 + 3 = 4
        self.assertEqual(4, channel.value)

    def test_right(self):
        length = 10
        delta = 1
        cycler = Cycler(length, delta, initial_position=8)
        self.assertEqual(9, cycler.value)
        keys = [(3, 3), (5, 2), (7, 5)]
        # (7, 5), (13, 3) = 5 - 2/6 * 2 =
        channel = cycler.channel(keys)
        self.assertAlmostEqual(4.33, channel.value, 2)

    def test_no_keys(self):
        cycler = Cycler(10, 1, initial_position=1)
        keys = []
        try:
            cycler.channel(keys)
            self.fail("Expected exception.")
        except RuntimeError:
            pass  # expected

    def test_keys_3_tuple(self):
        cycler = Cycler(10, 1, initial_position=1)
        keys = [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
        try:
            cycler.channel(keys)
            self.fail("Expected exception.")
        except RuntimeError:
            pass  # expected

    def test_one_key_left(self):
        cycler = Cycler(10, 1, initial_position=1)
        keys = [(3, 3)]
        channel = cycler.channel(keys)
        self.assertEqual(3, channel.value)

    def test_one_key_right(self):
        cycler = Cycler(10, 1, initial_position=5)
        keys = [(3, 3)]
        channel = cycler.channel(keys)
        self.assertEqual(3, channel.value)
