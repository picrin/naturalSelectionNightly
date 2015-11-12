from .testPointPicking import *
from .testSims import *
from .testGenerateGraph import *
import unittest
def runAll():
    runner = unittest.TextTestRunner(verbosity=2)
    load = unittest.TestLoader().loadTestsFromTestCase
    suite = load(TestSims)
    suite.addTests(load(TestPointPicking))
    suite.addTests(load(TestGenerateGraph))
    runner.run(suite)

