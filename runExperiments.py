from naturalSelection import *
import time
import sys
import os
import os.path
import random
import shutil
import scipy.stats
import json

random.seed(0)

ls = os.listdir
p = os.path.join
resultDir = "results"

redo = False
if "redo" in sys.argv:
    redo = True

def splitAndKeep(string, delimiters):
    currentLeft = 0
    for i, char in enumerate(string):
        if char in delimiters:
            yield string[currentLeft:i]
            yield string[i:i+1]
            currentLeft = i+1
    yield string[currentLeft:]

class s1(object):
    """
    Selective Sweep Dominant Wanderer Fitness Breeder Simulation.
    """
    def __init__(self):
        self.sizes = [100, 200]
        self.repetitions = 500
        self.generations = 100
        self.firstMutationAt = 0
        self.advantageRange = [1.05]
    def simulation(self, size, generations, firstMutationAt, advantage, repetition):
        filename = p(resultDir, "".join(map(str, ["_typ:sim", "_cla:", type(self).__name__, "_siz:" , size, "_gen:" , generations, "_mut:", firstMutationAt, "_adv:", advantage, "_rep:", repetition,"_sha:", sys.argv[1]])))
        def breeder(sims):
            return fitnessBreeder(sims, advantage, len(sims))
        def mutator(allSims):
            pass
        def firstMutator(allSims):
            randomSimIndex = random.randint(0, len(allSims) - 1)
            allSims[randomSimIndex]["genotype"]["hasCopy1"] = True
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
                        start = time.clock()
                        with open(temp_filename, "w") as result:
                            writePopulation(result, population)
                        shutil.move(temp_filename, filename)
                        stop = time.clock()
                        print(filename, str(stop - start))

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
                            mrcaFile.write(",")
                            proportion = alleleProportion(g, generation)
                            mrcaFile.write(str(proportion))
                            mrcaFile.write("\n")
                    stop = time.clock()
                    print(mrcaPath, str(stop - start))

class s2(object):
    """
    Including Simon's suggestion on running a simulation until feature is saturated.
    """
    def __init__(self):
        self.sizes = [100]
        self.repetitions = 200
        self.firstMutationAt = 0
        self.advantageRange = [1.1]
    
    def simulation(self, size, isControl, advantage, repetition):
        filename = p(resultDir, "".join(map(str, ["_typ:sim", "_cla:", type(self).__name__, "_siz:" , size, "_isControl:", isControl ,"_adv:", advantage, "_rep:", repetition,"_sha:", sys.argv[1]])))
        def breeder(sims):
            return fitnessBreeder(sims, advantage, len(sims))
        def mutator(allSims):
            pass
        def firstMutator(allSims):
            randomSimIndex = random.randint(0, len(allSims) - 1)
            allSims[randomSimIndex]["genotype"]["hasCopy1"] = True
            for sim in allSims:
                sim["genotype"]["isDominant"] = True
        def firstGeneration():
            return simsFrame(populationSize = size, mutator = firstMutator)
        def nextGeneration(nextFrame):
            return nextFrame(migrator = wandererMigrator, breeder = breeder, mutator = mutator)
        return generatePopulationPure(2**32, firstGeneration, nextGeneration), filename
    
    def controlSimulation(self, size, isControl, advantage, repetition, generations):
        filename = p(resultDir, "".join(map(str, ["_typ:sim", "_cla:", type(self).__name__, "_siz:" , size, "_isControl:", isControl ,"_adv:", advantage, "_rep:", repetition,"_sha:", sys.argv[1]])))
        def breeder(sims):
            return fitnessBreeder(sims, advantage, len(sims))
        def mutator(allSims):
            pass
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
                    def cond(sims):
                        proportion = alleleProportionSims(sims)
                        lucky = proportion == size*2
                        unlucky = proportion == 0
                        if lucky:
                            luckState["v"] = True
                        if unlucky:
                            luckState["v"] = False
                        writtenGen["v"] += 1
                        return not (lucky or unlucky)
                    population, filename = self.simulation(size, False, advantage, repetition)
                    if not os.path.isfile(filename) or redo:
                        luckState = {"v": False}
                        #compute and write sample
                        temp_filename = "tmp_" + str(random.randint(0, 10**12))
                        start = time.clock()
                        while not luckState["v"]:
                            writtenGen = {"v": 0}
                            with open(temp_filename, "w") as result:
                                writePopulationConditional(result, population, cond)
                            population, filename = self.simulation(size, False, advantage, repetition)
                        shutil.move(temp_filename, filename)
                        stop = time.clock()
                        print(filename, str(stop - start))
                        
                        #compute and write control
                        controlPop, filename = self.controlSimulation(size, True, advantage, repetition, writtenGen["v"] - 1)
                        temp_filename = "tmp_" + str(random.randint(0, 10**12))
                        start = time.clock()
                        with open(temp_filename, "w") as result:
                            writePopulation(result, controlPop)
                        shutil.move(temp_filename, filename)
                        stop = time.clock()
                        print(filename, str(stop - start))

class mrca2(s2):
    def __init__(self):
        pass
    def mrcaCompute(self, control):
        lsresult = ls(resultDir)
        mrcaResults = {}
        for path in lsresult:
            print("*")
            terms = list(splitAndKeep(path, ["_", ":"]))
            typeIndex = terms.index("typ")
            if terms[typeIndex + 2] == "sim":
                size = int(terms[terms.index("siz") + 2])
                rawIsControl = terms[terms.index("isControl") + 2]
                if rawIsControl == "True":
                    isControl = True
                else:
                    isControl = False
                if isControl == control:
                    with open(p(resultDir, path)) as fileName:
                        g = loadGraph(fileName)
                    generations = len(g["generations"])
                    generation = generations/2
                    T_mrca = quickMRCA(g, generation, size)[1]
                    if size in mrcaResults:
                        mrcaResults[size].append(T_mrca)
                    else:
                        mrcaResults[size] = [T_mrca]
        return mrcaResults
    def run(self):
        lsresult = ls(resultDir)
        if "mrca2" not in lsresult:
            samples = self.mrcaCompute(False)
            controls = self.mrcaCompute(True)
            for key in samples:
                sample = samples[key]
                control = controls[key]
                with open(p(resultDir, "mrca2"), "w") as r:
                    json.dump({"sample":sample, "control": control}, r)

class proc2(mrca2):
    def __init__(self):
        pass
    def run(self):
        with open(p(resultDir, "mrca2"), "r") as r:
            data = json.load(r)
            for s in ["sample", "control"]:
                print(s)
                print(scipy.average(data[s]))
                print(scipy.median(data[s]))
                print(min(data[s]))
                print(max(data[s]))
                print(scipy.stats.mode(data[s]))
            print("Ties corrected Mann-Whitney U-test for population of size:")
            print(scipy.stats.mannwhitneyu(data["sample"], data["control"]))
            print("Continuous Kologomorov-Smirnov. Ununjusted for discrete values! For population of size:")
            print(scipy.stats.ks_2samp(data["sample"], data["control"]))

def workflow(classa):
    simulation = classa()
    simulation.prep()
    simulation.run()

if "s1" in sys.argv:
    workflow(s1)

if "s2" in sys.argv:
    workflow(s2)

if "mrca" in sys.argv:
    workflow(mrca)
    
if "mrca2" in sys.argv:
    workflow(mrca2)

if "proc2" in sys.argv:
    workflow(proc2)

