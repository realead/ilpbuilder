import unittest

import ilpbuilder

 
class ExecutorTester(unittest.TestCase):  
    def test_ilpbuilder_version(self):
        self.assertEqual(ilpbuilder.__version__[0], 0)
        self.assertEqual(ilpbuilder.__version__[1], 1)
        self.assertEqual(ilpbuilder.__version__[2], 0)
