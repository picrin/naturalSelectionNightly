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

redo = False
if "redo" in sys.argv:
    redo = True

class s1(object):
    """
    Selective Sweep Dominant Wanderer Fitness Breeder Simulation.
    """
    def __init__(self):
        self.counter = 0
        self.sizes = [100]
        self.repetitions = 3
        self.generations = 100
        self.firstMutationAt = 50
        self.advantageRange = [1.05]
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
        for repetition in range(self.repetitions):
            for advantage in self.advantageRange:
                for size in self.sizes:
                    population, filename = self.simulation(size, self.generations, self.firstMutationAt, advantage, repetition)
                    if not os.path.isfile(filename) or redo:
                        temp_filename = "tmp_" + str(random.randint(0, 10**12))
                        with open(temp_filename, "w") as result:
                            writePopulation(result, population)
                            print(filename)
                            shutil.move(temp_filename, filename)

class mrca(s1):
    def __init__(self):
        pass
    def run(self):
        lsresult = ls(resultDir)
        for result in lsresult:
            terms = list(splitAndKeep(result, ["_", ":"]))
            typeIndex = terms.index("typ")
            if terms[typeIndex + 2] == "sim":
                size = int(terms[terms.index("siz") + 2])
                terms[typeIndex + 2] = "mrca"
                mrcaPath = p(resultDir, "".join(terms))
                if not os.path.isfile(mrcaPath) or redo:
                    with open(p(resultDir, result), "r") as graphFile:
                        g = loadGraph(graphFile)
                    generations = len(g["generations"])
                    start = time.clock()
                    with open(mrcaPath, "w") as mrcaFile:
                        for generation in range(generations):
                            mrca = quickMRCA(g, generation, size)
                            mrcaFile.write(str(mrca[1]))
                            mrcaFile.write("\n")
                    stop = time.clock()
                    print(mrcaPath, str(stop - start))

def workFlow(classa):
    simulation = classa()
    simulation.prep()
    simulation.run()

if "s1" in sys.argv:
    workFlow(s1)

def splitAndKeep(string, delimiters):
    currentLeft = 0
    for i, char in enumerate(string):
        if char in delimiters:
            yield string[currentLeft:i]
            yield string[i:i+1]
            currentLeft = i+1
    yield string[currentLeft:]

if "mrca" in sys.argv:
    workFlow(mrca)
