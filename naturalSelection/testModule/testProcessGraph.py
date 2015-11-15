from ..processGraph import *
import unittest
class TestProcessGraph(unittest.TestCase):
    def testValidJson(self):
        """
        tests file dropped by testGenerateGraph is a valid json
        """
        with open(".testParentChild") as f:
            g = loadGraph(f)
