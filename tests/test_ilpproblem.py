import unittest

from ilpbuilder.ilpproblem import ILConstrain

 
class ILConstrainTester(unittest.TestCase): 
   def test_empty(self):
        c1=ILConstrain(ILConstrain.LESS)
        with self.assertRaises(Exception) as context:
            c1.toString()
        self.assertTrue('no coeffs in constrain' in str(context.exception))

   def test_no_result(self):
        c1=ILConstrain(ILConstrain.LESS)
        c1.add_coeff("x1", 3)
        c1.add_coeff("x2", -4)
        with self.assertRaises(Exception) as context:
            c1.toString()
        self.assertTrue('result of this constrain is unknown' in str(context.exception))

   def test_with_result(self):
        c1=ILConstrain(ILConstrain.LESS)
        c1.add_coeff("x1", 3)
        c1.add_coeff("x2", -4)
        c1.set_result(1)
        self.assertEqual(c1.toString(), "3 x1 - 4 x2 < 1")

   def test_with_name(self):
        c1=ILConstrain(ILConstrain.LESS)
        c1.add_coeff("x1", 3)
        c1.add_coeff("x2", -4)
        c1.set_result(1)
        c1.set_name("c1")
        self.assertEqual(c1.toString(), "c1: 3 x1 - 4 x2 < 1")


   def test_with_result2(self):
        c1=ILConstrain(ILConstrain.LESS)
        c1.add_coeff("x1", 3)
        c1.add_coeff("x2", -4)
        c1.set_result(1)
        c1.add_coeff("x3",-3)
        self.assertEqual(c1.toString(), "3 x1 - 4 x2 - 3 x3 < 1")
 
