from ..sims import *
from ..pointPicking import *
import unittest
import random
random.seed(11)
class TestSims(unittest.TestCase):
    def testSimsBreed(self):
        simA = createRandomlyPositionedSim()
        simA["gender"] = True
        simB = createRandomlyPositionedSim()
        simB["gender"] = False
        simC = createSimFromParents(simA, simB)
        self.assertTrue(simB["pos"] == simC["pos"])
    def testRandomGeneCopy(self):
        simA = createRandomlyPositionedSim()
        simA["genotype"]["hasCopy1"] = True
        simA["genotype"]["hasCopy2"] = True
        self.assertTrue(getRandomGeneCopy(simA))
        simA["genotype"]["hasCopy1"] = False
        simA["genotype"]["hasCopy2"] = False
        self.assertTrue(not getRandomGeneCopy(simA))
    def testHasFeature(self):
        simA = makeDominant(createRandomlyPositionedSim())
        self.assertTrue(not hasFeature(simA))
        simA["genotype"]["hasCopy1"] = True
        self.assertTrue(hasFeature(simA))
        simA["genotype"]["hasCopy2"] = True
        self.assertTrue(hasFeature(simA))
        makeRecessive(simA)
        self.assertTrue(hasFeature(simA))
        simA["genotype"]["hasCopy1"] = False
        self.assertTrue(not hasFeature(simA))
        simA["genotype"]["hasCopy2"] = False
        self.assertTrue(not hasFeature(simA))
    def testIterativeHomebody(self):
        """ Impressive, I can get 10^-17 accuracy in the point staying
        within the radius of the unit sphere, even when accumulating
        error 100 thousand times. I wonder if somehow the error cancels
        out, or if it is genuinly computers being so precise these days.
        """ 
        simA = createRandomlyPositionedSim()
        for i in range(1 * 1000):
            position1 = simA["pos"]
            goNoFarther = 1
            position2 = moveHomebody(simA, goNoFarther)
            distance = sphereDistance(position2, position1)
            self.assertTrue(distance < goNoFarther)
        self.assertAlmostEquals(sum(list(map(lambda c: c ** 2, polarToXYZ(simA["pos"])))), 1, delta=10 ** (-17) )