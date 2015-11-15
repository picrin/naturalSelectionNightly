from .pointPicking import *
from .sims import *
from .pointPicking import *
import random, bisect
import json


def trackSim(sim, allSims):
    allSims.append(sim)

def computeDistances(sim, distances):
    pass
    
def oneDominantAlleleMutator(allSims):
    for sim in allSims:
        sim["genotype"]["isDominant"] = True
    randomSimIndex = random.randint(0, len(allSims) - 1)
    allSims[randomSimIndex]["genotype"]["hasCopy1"] = True

def generatePossibleCouples(sims):
    for simAI, simA in enumerate(sims):
        for simB in sims[simAI+1:]:
            if simA["isMale"] != simB["isMale"]:
                yield simA, simB

def simpleProximityBreeder(sims):
    """
    child distribution is given by the following discrete probability distribution function:
    f(0) = 0.18
    f(1) = 0.1
    f(2) = 0.4
    f(3) = 0.2
    f(4) = 0.1
    f(5) = 0.02
    Expected value of f is 2.0, and that's why it was decided to be a good simple choice,
    as it both captures the intuition that most likely outcomes of mating are 2 children and
    it won't lead to quick exponential growth.
    """
    f0 = 0.18
    f1 = 0.1
    f2 = 0.4
    f3 = 0.2
    f4 = 0.1
    f5 = 0.02
    pdf = [f0, f1, f2, f3, f4, f5]
    cdf = []
    current = 0
    for i in pdf:
        current += i
        cdf.append(current)
    assert(cdf[-1] == 1)
    couples = proximityMater(sims)
    newSims = []
    for couple in couples:
        randomChildren = random.uniform(0, sum(pdf))
        for childrenNo, threshold in enumerate(cdf):
            if randomChildren < threshold:
                break
        newSims += [createSimFromParents(*couple) for i in range(childrenNo)]
    return newSims
    
def constantBreeder(sims):
    couples = proximityMater(sims)
    newSims = []
    for couple in couples:
        childrenNo = 3
        newSims += [createSimFromParents(*couple) for i in range(childrenNo)]
    return newSims

def proximityMater(sims):
    proximityPossibleCouples = []
    takenSims = {}
    for possibleCouple in generatePossibleCouples(sims):
        positionA = possibleCouple[0]["pos"]
        positionB = possibleCouple[1]["pos"]
        howClose = sphereDistance(positionA, positionB)
        proximityPossibleCouples.append([howClose, possibleCouple,])
    proximityPossibleCouples.sort(key = lambda n: n[0])
    actualCouples = []

    for distanceCouple in proximityPossibleCouples:
        couple = distanceCouple[1]
        if couple[0]["uid"] not in takenSims and couple[1]["uid"] not in takenSims:
            takenSims[couple[0]["uid"]] = True
            takenSims[couple[1]["uid"]] = True
            actualCouples.append(couple)
    return actualCouples

def simsFrame(sims = None, populationSize = 0, mutator = None, breeder=None, migrator=None):
    """
    if the breeder is not None, the mutator is applied after the breeder, and it's applied to children.
    if the breeder is None, there is no breeding, there is no children, and the mutator is applied to the sims passed in, or the first-generation sims.
    if the breeder is None, the return value is the sims passed in, or generated first-generation sims.
    """
    stopBreeding = False
    if sims is None:
        stopBreeding = True
        if populationSize > 0:
            sims = [createRandomlyPositionedSim() for i in range(populationSize)]
        else:
            raise ValueError("allSims and populationSize can't be both default")
    if breeder is not None and not stopBreeding:
        sims = breeder(sims)
    if mutator is not None:
        mutator(sims)
    if migrator is not None:
        migrator(sims)
    def nextFrame(**kwargs):
        if "sims" not in kwargs:
            kwargs["sims"] = sims
        return simsFrame(**kwargs)
    return sims, nextFrame

def wandererMigrator(sims):
    for sim in sims:
        moveWanderer(sim)

def serialiseSim(sim, first = False, last = False):
    shallowCopyNoParents = {}
    for key in sim:
        if key not in ["parentA", "parentB"]:
            shallowCopyNoParents[key] = sim[key]
        else:
            if sim[key] is not None:
                shallowCopyNoParents[key] = sim[key]["uid"]
            else:
                shallowCopyNoParents[key] = None
    if first:
        shallowCopyNoParents["generation"] = "first"
    if last:
        shallowCopyNoParents["generation"] = "last"
    if not first and not last:
        shallowCopyNoParents["generation"] = "middle"
    return shallowCopyNoParents

def generateToyPopulation(fileObj):
    """
    this gives a population, which has one sim who is a carrier of a dominant allele.
    The population then evolves for 3 generations (achieving total of 4 generations) using the wanderer model of
    migration and the simpleProximityBreeder.
    """
    def firstGeneration():
       return simsFrame(populationSize = 10, mutator = oneDominantAlleleMutator)
    def nextGeneration(nextFrame):
       return nextFrame(migrator=wandererMigrator, breeder=simpleProximityBreeder)
    generatePopulation(fileObj, 3, firstGeneration, nextGeneration)

def generatePopulation(fileObj, generationNo, firstGeneration, nextGeneration):
    def writeAllSims(sims, first=False, last=False):
        firstSim = first
        if firstSim:
           fileObj.write("[")
        for i, sim in enumerate(sims):
            if not firstSim:
                fileObj.write(",\n")
            firstSim = False
            json.dump(serialiseSim(sim, first=first, last=last), fileObj)
    sims, nextFrame = firstGeneration()
    first = True
    for i in range(generationNo):
        writeAllSims(sims, first=first)
        first = False
        sims, nextFrame = nextGeneration(nextFrame)
    writeAllSims(sims, last=True)
    fileObj.write("]")
