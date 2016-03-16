import unittest
from ..generateGraph import * 
from ..pointPicking import *
from ..sims import *
from ..utils import *
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
    def testCondWriter(self):
        def nullMutator(sims):
            pass
        def firstGeneration():
            return simsFrame(populationSize = 100, mutator = nullMutator)
        def nextGeneration(nextFrame):
            return nextFrame(migrator = wandererMigrator, breeder = simpleProximityBreeder, mutator = nullMutator)
        def cond(sims):
            return False
        fail = {"v": 0}
        gens = generatePopulationPure(2**32, firstGeneration, nextGeneration)
        with open(".testCondWriter", "w") as testFile:
            writePopulationConditional(testFile, gens, cond)
        with open(".testCondWriter", "r") as testFile:
            def unpackLines(lines):
                for line in lines:
                    for char in line:
                        yield char
            mustBeTwoOhTwo = 0
            for char in unpackLines(testFile.readlines()):
                if char == "[" or char == "]":
                    mustBeTwoOhTwo += 1
        self.assertTrue(mustBeTwoOhTwo == 202)

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
        """
        Tests that the results of fitness breeder are within 5 sigma around mean.
        The feature boosts absolute fitness by the factor of 2.0
        The distribution is assumed to be binomial with the following probabilities:
        A = p(both parents have feature) = 2/3 * 1/2 = 1/3
        B = p(both parents have no feature) =  1/3 * 1/2  = 1/6
        C = p(exactly one parent has the feauture) = 2/3 * 1/2 + 1/3 * 1/2 = 1/2
        
        A + B + C = 1, as expected.
        
        D = p(at least one parent has no feature) =  C + B = 2/3
        E = p(at least one parent has a feature) = C + A = 5/6
        
        we then use standard deviation result for binomial distribution, say, repeated 100 times.
        The formula is sqrt(n(1-p)p).
        """
        totalSize = 100
        size = int(totalSize/2)

        D = 2.0/3
        E = 5.0/6
        D5sigma = sigmaBinomial(100, D, 5)
        E5sigma = sigmaBinomial(100, E, 5)
        self.assertAlmostEquals(D5sigma, 23.57, delta=0.1)
        self.assertAlmostEquals(E5sigma, 18.6, delta=0.1)
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
        self.assertTrue(-E5sigma <= successfulParents - E*totalSize <= E5sigma)
        self.assertTrue(-D5sigma <= unsuccessfulParents - D*totalSize <= D5sigma)
      
