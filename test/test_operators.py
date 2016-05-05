import unittest

from kabuki.operators import *


class TestAdd(unittest.TestCase):

    def test_simple(self):
        n1 = Operand(value=1.5)
        n2 = Operand(value=3.75)

        op = Add(n1, n2)
        self.assertEqual(5.25, op.value)

        n1.value = 1.75
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

        n.value = -1.7
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


class TestSub(unittest.TestCase):

    def test_simple(self):
        n1 = Operand(value=1.5)
        n2 = Operand(value=0.25)

        op = Sub(n1, n2)
        self.assertEqual(1.25, op.value)

        n1.value = 1.75
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

        n.value = -1.7
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

        n1.value = 6.3
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

        n1.value = 6.3
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
        self.assertEqual(3, n1.filter_above(n2).value)


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
        self.assertEqual(3, n1.filter_below(n2).value)


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