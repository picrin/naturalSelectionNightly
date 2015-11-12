import unittest
from ..generateGraph import * 
from ..pointPicking import *
from ..sims import *
import math
import random

def make4Sims():
    changeUID(0)
    
    simA = createSim()
    simA["pos"] = [50*dtr, 10*dtr]
    simA["isMale"] = True
    
    simB = createSim()
    simB["pos"] = [45*dtr, 15*dtr]
    simB["isMale"] = False
    
    simC = createSim()
    simC["pos"] = [-50*dtr, -15*dtr]
    simC["isMale"] = True
    
    simD = createSim()
    simD["pos"] = [-40*dtr, -6*dtr]
    simD["isMale"] = False
    return [simA, simB, simC, simD]

class TestGenerateGraph(unittest.TestCase):
    def testMater(self):
        sims = make4Sims()
        for i in range(100):
            random.shuffle(sims)
            couples = proximityMater(sims)
            for couple in couples:
                if couple[0]["uid"] == 0:
                    self.assertTrue(couple[1]["uid"] == 1)
                if couple[0]["uid"] == 1:
                   self.assertTrue(couple[1]["uid"] == 0)
                if couple[0]["uid"] == 2:
                   self.assertTrue(couple[1]["uid"] == 3)
                if couple[0]["uid"] == 3:
                   self.assertTrue(couple[1]["uid"] == 2)
    def testBreeder(self):
        sims = make4Sims()
        children = simpleProximityBreeder(sims)
        for child in children:
            self.assertTrue(child["parentA"] in sims and child["parentB"] in sims)            
    def testParentChildFirstPart(self):
        with open(".testParentChild", "w") as test:
            generateToyPopulation(test)

