from .testPointPicking import *
from .testSims import *
from unittest import *
runner = unittest.TextTestRunner(verbosity=2)
l = unittest.TestLoader().loadTestsFromTestCase
suite = l(TestSims)
suite.addTests(l(TestPointPicking))
runner.run(suite)

