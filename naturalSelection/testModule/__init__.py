from .testPointPicking import *
from .testSims import *
from .testGenerateGraph import *
from .testProcessGraph import *
import unittest
def runAll():
    runner = unittest.TextTestRunner(verbosity=2)
    load = unittest.TestLoader().loadTestsFromTestCase
    suite = load(TestSims)
    def add(testClass):
        suite.addTests(load(testClass))
    add(TestPointPicking)
    add(TestGenerateGraph)
    add(TestProcessGraph)
    runner.run(suite)

