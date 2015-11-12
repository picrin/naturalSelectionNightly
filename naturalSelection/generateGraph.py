from .pointPicking import *
from .sims import *
from .pointPicking import *
import random, bisect

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
    f(1) = 0.2
    f(2) = 0.5
    f(3) = 0.3
    Expected value of f is 2.1, and that's why it was decided to be a good simple choice,
    as it both captures the intuition that most likely outcomes of mating are 2 children and
    it won't lead to quick exponential growth.
    """
    couples = proximityMater(sims)
    newSims = []
    for couple in couples:
        randomChildren = random.uniform(0, 1)
        if randomChildren < 0.2:
            childrenNo = 1
        elif randomChildren < 0.7:
            childrenNo = 2
        else:
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
    #print("possible couples")
    #print([[couple[0], [couple[1][0]["isMale"], couple[1][1]["isMale"]]] for couple in proximityPossibleCouples])
    #print("end possible couples")
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
        #print ("shouldn't be None", sims)
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

def generateToyPopulation(fileObj):
    """
    this gives a very small, initially 4 sims population, which has one sim who is a carrier of a dominant allele.
    The population then evolves for 3 generations (achieving total of 4 generations) using the wanderer model of
    migration and the simpleProximityBreeder.
    """
    def writeAllSims(sims):
        for sim in sims:
            fileObj.write(str(simToTuple(sim)) + "\n")
    sims, nextFrame = simsFrame(populationSize = 4, mutator = oneDominantAlleleMutator)
    for i in range(3):
        writeAllSims(sims)
        sims, nextFrame = nextFrame(migrator=wandererMigrator, breeder=simpleProximityBreeder)
    writeAllSims(sims)
