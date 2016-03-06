from naturalSelection import *
initialSize = 200
generations = 700
firstMutationAt = 10
count = 0

def SSDWFBS(size, generations):
    """
    stands for Selective Sweep Dominant Wanderer Fitness Breeder Simulation.
    """
    def firstGeneration():
       return simsFrame(populationSize = size, mutator = firstMutator)
    def nextGeneration(nextFrame):
       return nextFrame(migrator=wandererMigrator, breeder=slimAdvantageFitnessBreeder, mutator = dominantSingleAlleleMutator)
    return generatePopulationPure(generations, firstGeneration, nextGeneration)

def firstMutator(allSims):
    for sim in allSims:
        sim["genotype"]["isDominant"] = True
    dominantSingleAlleleMutator(allSims)

def dominantSingleAlleleMutator(allSims): 
    global count
    if count == firstMutationAt:
        randomSimIndex = random.randint(0, len(allSims) - 1)
        allSims[randomSimIndex]["genotype"]["hasCopy1"] = True
    count += 1

#def smallFractionDominantMutator(allSims):
#    for sim in allSims:
#        sim["genotype"]["isDominant"] = True
#    for i in range(len(allSims)/10):
#        randomSimIndex = random.randint(0, len(allSims) - 1)
#        allSims[randomSimIndex]["genotype"]["hasCopy1"] = True
#        allSims[randomSimIndex]["genotype"]["hasCopy2"] = True

import time
import sys
filename = "fitnessBreederResults/checkMRCA"
with open(filename, "w") as result:
    writePopulation(result, SSDWFBS(initialSize, generations))

with open(filename, "r") as result:
    simulation = loadGraph(result)
    print(quickMRCA(simulation, -1, 2**64))
#for filename in range(100):
#    count = 0
#    with open("fitnessBreederResults/" + str(filename), "w") as result:
#        for generation in SSDWFBS(initialSize, generations):
#            result.write(str(count) + " " + str(sum(map(hasFeature, generation))) + "\n")

"""
filenameSuffix = 1

for result in results:
    print(result["initialSize"], result["generations"])
    simulation = list(noGenesWanderers(result["initialSize"], result['generations']))
    sizePerGeneration = []
    for generation in simulation:
        sizePerGeneration.append(len(generation))
    path = "./results/noGenesWanderers" + str(filenameSuffix)
    filenameSuffix += 1
    with open(path, "w") as fileobj:
        writePopulation(fileobj, (generation for generation in simulation))
    with open(path, "r") as fileobj:
        simulation = loadGraph(fileobj)
    result["sizePerGeneration"] = sizePerGeneration
    result["MRCA"] = MRCA(simulation)[1]
    result["filename"] = path
    
print(results)
"""
