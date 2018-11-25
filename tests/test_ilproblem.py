import unittest

from ilpbuilder.ilproblem import ILConstrain, ILProblem

from ilpbuilder.ilpexport import IBMLPExporter, LPExporter



 
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


class ILProblemTester(unittest.TestCase): 

   def test_construct_simple_ibm(self):
        c1=ILConstrain(ILConstrain.LESS_EQUAL, result = 1, name="c1")
        c1.add_coeff("x1", 1)
        c1.add_coeff("x2", 1)

        problem = ILProblem()
        problem.define_as_bin_vars({'x1','x2'})
        problem.set_cost_fun({'x1':10, 'x2' : 3})
        problem.add_constrain(c1)

        exporter = IBMLPExporter()
        problem.export(exporter)

        expected = ["MINIMIZE\n",
                    " obj: 10 x1 + 3 x2 \n", 
                    "Subject To\n",
                    " c1: 1 x1 + 1 x2 <= 1\n",
                    "BINARY\n",
                    " x1 x2\n",
                    "GENERAL\n",
                    " \n",
                    "END\n"]

        received = exporter.get_lines()
        self.assertEqual(expected, received)

   def test_construct_simple_lp(self):
        c1=ILConstrain(ILConstrain.LESS_EQUAL, result = 1, name="c1")
        c1.add_coeff("x1", 1)
        c1.add_coeff("x2", 1)

        problem = ILProblem('max')
        problem.define_as_bin_vars({'x1','x2'})
        problem.set_cost_fun({'x1': 10, 'x2' : 3})
        problem.add_constrain(c1)

        exporter = LPExporter()
        problem.export(exporter)


        expected = ["/* model created by ilpbuilder */\n",
                    "\n",
                    "max: 10 x1 + 3 x2 ;\n",
                    "\n",
                    "c1: 1 x1 + 1 x2 <= 1;\n",
                    "\n",
                    "bin x1, x2;\n",
                    "int ;\n"]

        received = exporter.get_lines()
        self.assertEqual(expected, received)


        
 
