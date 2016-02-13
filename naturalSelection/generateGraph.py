from .pointPicking import *
from .sims import *
from .pointPicking import *
import random, bisect
import json, sys

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
    Expected value of f is 2.05, and that's why it was decided to be a good simple choice,
    as it both captures the intuition that most likely outcomes of mating are about 2 children and
    it won't lead to quick exponential growth for large populations, and for small populations it makes
    the population less likely to die off due to random male/female imbalances.
    """
    f0 = 0.17
    f1 = 0.1
    f2 = 0.4
    f3 = 0.2
    f4 = 0.1
    f5 = 0.03
    pdf = [f0, f1, f2, f3, f4, f5]
    return proximityBreeder(sims, pdf)
    
def proximityBreeder(sims, pdf):
    cdf = []
    current = 0
    for i in pdf:
        current += i
        cdf.append(current)
    #assert(cdf[-1] == 1)
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
        childrenNo = 2
        newSims += [createSimFromParents(*couple) for i in range(childrenNo)]
    return newSims

def slimAdvantageFitnessBreeder(sims):
    return fitnessBreeder(sims, 1.05, len(sims))

def constructFitnessCDF(sims):
    """
    Creates a python list representing a (discrete) cumulative distribution function, which can be used to sample sims with probability relative to their fitness.
    """
    cdf = [sims[0]["absoluteFitness"]]
    for sim in sims[1:]:
        cdf.append(cdf[-1] + sim["absoluteFitness"])
    return cdf

def sampleFromFitnessCDF(cdf, randomFloat0to1):
    return bisect.bisect_left(cdf, randomFloat0to1 * cdf[-1])
 
def fitnessBreeder(sims, ratio, reproductionCap):
    """
    Breeder based on the the idea introduced in [TODO peng's paper]. The pdf of offspring is binomial. The sampling is based on relative fitness. Number of individuals is kept constant.
    """
    for sim in sims:
        adjustAbsoluteFitness(sim, ratio)
    nextSims = []
    while(len(nextSims) < reproductionCap):
        cdf = constructFitnessCDF(sims)
        random0to1 = random.uniform(0, 1)
        toReproduce = sampleFromFitnessCDF(cdf, random0to1)
        simFrom = sims[toReproduce]
        coupleGen = coupleGeneratorFrom(simFrom)
        allPossibleCouples = proximityCoupling(coupleGen, sims)
        closestCouple = allPossibleCouples[0][1]
        nextSim = createSimFromParents(*closestCouple)
        nextSims.append(nextSim)
    return nextSims

def coupleGeneratorFrom(simFrom):
    def generator(sims):
        return generatePossibleCouplesFrom(simFrom, sims)
    return generator

def generatePossibleCouplesFrom(simFrom, sims):
    for sim in sims:
        if sim["isMale"] != simFrom["isMale"]:
            yield simFrom, sim


def proximityCoupling(coupleGenerator, sims):
    proximityPossibleCouples = []
    for possibleCouple in coupleGenerator(sims):
        positionA = possibleCouple[0]["pos"]
        positionB = possibleCouple[1]["pos"]
        howClose = sphereDistance(positionA, positionB)
        proximityPossibleCouples.append([howClose, possibleCouple,])
    proximityPossibleCouples.sort(key = lambda n: n[0])
    return proximityPossibleCouples
    

def proximityMater(sims):
    """
    Breeds those male-female pairs which are the closest on the surface of the sphere. The algorithm is greedy, in a sense that the smallest distance couple is guaranteed
    to be together, after which they're both removed from the set of possible couples, and the mating continues with the next smallest distance couple.
    """
    actualCouples = []
    takenSims = {}
    proximityPossibleCouples = proximityCoupling(generatePossibleCouples, sims)
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
        
def homebodyMigrator(sims):
    for sim in sims:
        moveHomebody(sim)

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

def generatePopulationPure(generationNo, firstGeneration, nextGeneration):
    """
    Population is generated using functions firstGeneration and nextGeneration. Simulation is continued for generationNo discrete generations, generationNo must be greater than 1.
    For a good example usage look at the implementation of generateToyPopulation, especially how to define firstGeneration and nextGeneration.
    """    
    sims, nextFrame = firstGeneration()
    yield sims
    for i in range(generationNo):
        sims, nextFrame = nextGeneration(nextFrame)
        yield sims

def generatePopulation(fileObj, generationNo, firstGeneration, nextGeneration):
    allSims = generatePopulationPure(generationNo, firstGeneration, nextGeneration)
    writePopulation(fileObj, allSims)
    
def writePopulation(fileObj, generations):
    """
    Writes json representation of a generated population to a file.
    """
    def writeAllSims(sims, first=False, last=False):
        firstSim = first
        if firstSim:
           fileObj.write("[")
        for i, sim in enumerate(sims):
            if not firstSim:
                fileObj.write(",\n")
            firstSim = False
            json.dump(serialiseSim(sim, first=first, last=last), fileObj) 
    sims = next(generations)
    first = True
    for nextSims in generations:
        writeAllSims(sims, first=first)
        first = False
        sims = nextSims
    writeAllSims(sims, last=True)
    fileObj.write("]")
    pass
