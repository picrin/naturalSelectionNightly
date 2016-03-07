from naturalSelection import *
import time
import sys
import os
import os.path
import random
import shutil

random.seed(0)

ls = os.listdir
p = os.path.join
resultDir = "results"

import shutil

class s1(object):
    """
    Selective Sweep Dominant Wanderer Fitness Breeder Simulation.
    """
    def __init__(self):
        self.counter = 0
        self.sizes = [100]
        self.repetitions = 3
        self.generations = 30
        self.firstMutationAt = 100
        self.advantageRange = [1.01, 1.05, 1.10]
    def simulation(self, size, generations, firstMutationAt, advantage, repetition):
        filename = p(resultDir, "".join(map(str, ["_typ:sim", "_cla:", type(self).__name__, "_siz:" , size, "_gen:" , generations, "_mut:", firstMutationAt, "_adv:", advantage, "_rep:", repetition,"_sha:", sys.argv[1]])))
        def breeder(sims):
            return fitnessBreeder(sims, advantage, len(sims))
        def mutator(allSims):
            if self.counter == firstMutationAt:
                randomSimIndex = random.randint(0, len(allSims) - 1)
                allSims[randomSimIndex]["genotype"]["hasCopy1"] = True
            self.counter += 1
        def firstMutator(allSims):
            for sim in allSims:
                sim["genotype"]["isDominant"] = True
        def firstGeneration():
            return simsFrame(populationSize = size, mutator = firstMutator)
        def nextGeneration(nextFrame):
            return nextFrame(migrator = wandererMigrator, breeder = breeder, mutator = mutator)
        return generatePopulationPure(generations, firstGeneration, nextGeneration), filename
    def prep(self):
        try:
            os.makedirs(resultDir)
        except OSError as e:
            if e.errno != 17:
                raise(e)
    def run(self):
        self.prep()
        for repetition in range(self.repetitions):
            for advantage in self.advantageRange:
                for size in self.sizes:
                    population, filename = self.simulation(size, self.generations, self.firstMutationAt, advantage, repetition)
                    if not os.path.isfile(filename):
                        temp_filename = "tmp_" + str(random.randint(0, 10**12))
                        with open(temp_filename, "w") as result:
                            writePopulation(result, population)
                            print(filename)
                            shutil.move(temp_filename, filename)
                        
if "s1" in sys.argv:
    simulation = s1()
    simulation.run()

if "checkPreserved" in sys.argv:
    pass

if "mrca" in sys.argv:
    lsresult = ls(resultDir)
    relevant = []
    for path in lsresult:
        if "_mrca:y" not in path:
            relevant.append(path)
    for filename in relevant:
        fullPath = p(resultDir, filename)
        mrcaPath = fullPath + "_mrca:y"
        if not os.path.isfile(mrcaPath):
            with open(fullPath, "r") as graphFile:
                g = loadGraph(graphFile)
            start = time.clock()
            with open(mrcaPath, "w") as mrcaFile:
                mrca = quickMRCA(g, -1, 100)
                mrcaFile.write(str(mrca))
                mrcaFile.write("\n")
                mrcaFile.write(str(time.clock() - start))
                print(mrcaPath)
