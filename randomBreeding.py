import naturalSelection as ns
def generateRandomBreeding(fileObj):
    def firstGeneration():
       return ns.simsFrame(populationSize = 100, mutator = ns.oneDominantAlleleMutator)
    def nextGeneration(nextFrame):
       return nextFrame(migrator = ns.wandererMigrator, breeder = ns.simpleProximityBreeder)
    ns.generatePopulation(fileObj, 10, firstGeneration, nextGeneration)

def generateMutationBreeding(fileObj):
    def firstGeneration():
       return ns.simsFrame(populationSize = 10, mutator = ns.oneDominantAlleleMutator)
    def nextGeneration(nextFrame):
       return nextFrame(migrator = ns.wandererMigrator, breeder = ns.simpleProximityBreeder)
    ns.generatePopulation(fileObj, 3, firstGeneration, nextGeneration)

randomBreeding = "data/randomBreeding"
solutions = []
for i in range(10):
    with open(randomBreeding + str(i), 'w') as fileObj:
        generateRandomBreeding(fileObj)
    with open(randomBreeding + str(i), 'r') as fileObj:
        simulation = ns.loadGraph(fileObj)
    solutions.append(ns.MRCA(simulation)[1])
print solutions
