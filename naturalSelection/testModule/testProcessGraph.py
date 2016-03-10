from ..processGraph import *
import unittest
class TestProcessGraph(unittest.TestCase):
    def testValidJson(self):
        """
        tests file dropped by testGenerateGraph is a valid json
        """
        with open(".testParentChild") as f:
            g = loadGraph(f)
    def testValidGenerationNumbers(self):
        with open(".testParentChild") as f:
            g = loadGraph(f)
            self.assertTrue(len(g["generations"][0]) == 10)
            for generationNo, generation in enumerate(g["generations"]):
                for id in generation:
                    simsGenerationNo = getSimByID(g, id)["generationNo"]
                    self.assertTrue(simsGenerationNo == generationNo)
    def testTracers(self):
        """
        checks if tracers of the 0th generation are set appropriately from the first generation.
        """
        with open("satAncestryTestCase") as f:
            g = loadGraph(f)
        translation, reverseTranslation = initTracers(g, g["generations"][1])
        
        for simID in g["generations"][1]:
            sim = getSimByID(g, simID)
            for parentID in sim["parentA"], sim["parentB"]:
                getSimByID(g, parentID)["children"].append(simID)
        
        for parentID in g["generations"][0]:
            computeTracer(g, parentID)
        
        for i, simID in enumerate(g["generations"][1]):
            sim = getSimByID(g, simID)
            simPosition = reverseTranslation[simID]
            for parentID in sim["parentA"], sim["parentB"]:
                self.assertTrue(getSimByID(g, parentID)["tracers"][simPosition])
    def testSatQuickMRCA(self):
        with open("satAncestryTestCase") as f:
            g = loadGraph(f)
        call = quickMRCA(g, 3, 100000)
        self.assertTrue(call == (6, 2))
    def testRepeatedMRCA(self):
        with open("satAncestryTestCase") as f:
            g = loadGraph(f)
        call = quickMRCA(g, 3, 100000)
        call = quickMRCA(g, 3, 100000)
        self.assertTrue(call == (6, 2))
    def testUnsatQuickMRCA(self):
        with open("unsatAncestryTestCase") as f:
            g = loadGraph(f)
        call = quickMRCA(g, 3, 100000)
        self.assertTrue(call == (None, None))
    def testRandomMRCA(self):
        with open("randomAncestryTestCase") as f:
            g = loadGraph(f)
        call = quickMRCA(g, -1, 100000)
    def testMRCA(self):
        with open("satAncestryTestCase") as f:
            g = loadGraph(f)
        _, genOld = MRCA(g)
        _, genNew = quickMRCA(g, -1, 2**64)
        self.assertTrue(genOld == genNew)
    def testFeatureProportion(self):
        with open("randomAncestryTestCase") as handle:
            g = loadGraph(handle)
        self.assertTrue(featureProportion(g, 0) == 0)
        self.assertTrue(featureProportion(g, 1) == 1)
        self.assertTrue(featureProportion(g, 2) == 1)
        self.assertTrue(featureProportion(g, 3) == 2)
    def testAlleleProportion(self):
        with open("randomAncestryTestCase") as handle:
            g = loadGraph(handle)
        self.assertTrue(alleleProportion(g, 0) == 0)
        self.assertTrue(alleleProportion(g, 1) == 2)
        self.assertTrue(alleleProportion(g, 2) == 1)
        self.assertTrue(alleleProportion(g, 3) == 2)
