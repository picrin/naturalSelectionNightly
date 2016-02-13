import unittest
from ..generateGraph import * 
from ..pointPicking import *
from ..sims import *
import math
import sys
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
    def testParentChildFirstPart(self):
        """
        drops a file for future testProcessGraph
        """
        with open(".testParentChild", "w") as test:
            generateToyPopulation(test)
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
    def testMater2(self):
        sims, _ = simsFrame(populationSize=50)
        menNo = len([sim for sim in sims if sim["isMale"]])
        womenNo = len([sim for sim in sims if sim["isMale"] == False])
        couples = proximityMater(sims)
        self.assertTrue(min(womenNo, menNo) == len(couples))
    def testFitnessCDF(self):
        sims = [{"absoluteFitness": 1.0}, {"absoluteFitness": 2.0}]
        cdf = constructFitnessCDF(sims)
        for pair in zip(cdf, [1.0, 3.0]):
            self.assertTrue(pair[0], pair[1])
        self.assertTrue(sampleFromFitnessCDF(cdf, 0.8/3) == 0)
        self.assertTrue(sampleFromFitnessCDF(cdf, 1.2/3) == 1)
        self.assertTrue(sampleFromFitnessCDF(cdf, 2.9/3) == 1)
        self.assertTrue(sampleFromFitnessCDF(cdf, 3.0/3) == 1)
    def testFitnessBreeder(self):
        size = 4000
        totalSize = size*2
        unsuccessfulSims = [createRandomlyPositionedSim() for i in range(size)]
        successfulSims = [createRandomlyPositionedSim() for i in range(size)]
        successfulSimsIDs = [sim["uid"] for sim in successfulSims]
        unsuccessfulSimsIDs = [sim["uid"] for sim in unsuccessfulSims]
        for sim in successfulSims:
            makeHomozygous(sim)
        for sim in unsuccessfulSims:
            cancelFeature(sim)
        sims = successfulSims + unsuccessfulSims
        for sim in sims:
            makeDominant(sim)
        nextGeneration = fitnessBreeder(sims, 2.0, len(sims))
        successfulParents = 0
        unsuccessfulParents = 0
        self.assertTrue(len(nextGeneration) == totalSize)
        for sim in nextGeneration:
            if sim["parentA"]["uid"] in successfulSimsIDs or sim["parentB"]["uid"] in successfulSimsIDs:
                successfulParents += 1
            if sim["parentA"]["uid"] in unsuccessfulSimsIDs or sim["parentB"]["uid"] in unsuccessfulSimsIDs:
                unsuccessfulParents += 1
            
        print("\nsuccessfulParents", successfulParents/float(totalSize))
        print("\nunsuccessfulParents", unsuccessfulParents/float(totalSize))
       
