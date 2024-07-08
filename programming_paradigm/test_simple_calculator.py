#Writing Unit Tests for a Simple Calculator Class
import unittest
from simple_calculator import SimpleCalculator

class TestSimpleCalculator(unittest.TestCase):

    def setUp(self):
        """Set up the SimpleCalculator instance before each test."""
        self.calc = SimpleCalculator()

    def test_addition(self):
        """Test the addition method."""
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(-5,-1), -6)
        self.assertEqual(self.calc.add(-5,0), -5)
        self.assertEqual(self.calc.add(-5,-1), -6)
        self.assertEqual(self.calc.add(-5.5,1), -4.5)
        self.assertEqual(self.calc.add(-5.5,1.5), -4.0)

        # Add more assertions to thoroughly test the add method.
    def test_subtraction(self):
        """Test the subtraction method."""
        self.assertEqual(self.calc.subtract(2, 3), -1)
        self.assertEqual(self.calc.subtract(-1, 1), -2)
        self.assertEqual(self.calc.subtract(-5,-1), -4)
        self.assertEqual(self.calc.subtract(-5,0), -5)
        self.assertEqual(self.calc.subtract(-5,-1), -4)
        self.assertEqual(self.calc.subtract(-5.5,1), -6.5)
        self.assertEqual(self.calc.subtract(-5.5,1.5), -7.0)
    
    def test_multiplication(self):
        """Test the multiply method."""
        self.assertEqual(self.calc.multiply(2, 3), 6)
        self.assertEqual(self.calc.multiply(-1, 1), -1)
        self.assertEqual(self.calc.multiply(-5,-1), 5)
        self.assertEqual(self.calc.multiply(-5,0), 0)
        self.assertEqual(self.calc.multiply(-5,-1), 5)
        self.assertEqual(self.calc.multiply(-5.5,1), -5.5)
        self.assertEqual(self.calc.multiply(-5.5,1.5), -8.25)

    def test_division(self):
        """Test the divide method."""
        self.assertEqual(self.calc.divide(9, 3), 3)
        self.assertEqual(self.calc.divide(-1, 1), -1)
        self.assertEqual(self.calc.divide(-5,-1), 5)
        self.assertEqual(self.calc.divide(-5,0), None)
        self.assertEqual(self.calc.divide(-5,-1), 5)
        self.assertEqual(self.calc.divide(-5.5,1), -5.5)
        self.assertEqual(self.calc.divide(-5.5,1.5), -3.6666666666666665)





