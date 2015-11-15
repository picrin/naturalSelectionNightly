import networkx
import json
import collections

def loadGraph(fileObj):
    simsGraph = networkx.DiGraph()
    sims = json.load(fileObj)
    first = []
    last = []
    for sim in sims:
        sim["visitedBy"] = -1
        sim["descendants"] = 0 
        simsGraph.add_node(sim["uid"], sim)
        for parent in ["parentA", "parentB"]:
            if sim[parent] is not None:
                simsGraph.add_edge(sim[parent], sim["uid"])
        if sim["generation"] == "last":
            last.append(sim["uid"])
        if sim["generation"] == "first":
            first.append(sim["uid"])
    simulation = {"graph": simsGraph, "firstGeneration": first, "lastGeneration": last}
    return simulation

def countDescendants(simulation):
    def countDescendantsInner(nodeID, uid):
        node = simulation["graph"].node[nodeID]
        if node["visitedBy"] == uid:
            return
        else:
            node["descendants"] += 1
            node["visitedBy"] = uid
            if node["parentA"] is not None:
                countDescendantsInner(node["parentA"], uid)
            if node["parentB"] is not None:
                countDescendantsInner(node["parentB"], uid)
    for nodeID in simulation["lastGeneration"]:
        countDescendantsInner(nodeID, nodeID)

def countFeatures(simulation):
    pass

def MRCA(simulation):
    countDescendants(simulation)
    fifo = {}
    for i in simulation["lastGeneration"]:
        fifo[i] = True
    lastGenerationCount = len(simulation["lastGeneration"])
    #print(lastGenerationCount)
    #print(simulation["lastGeneration"])
    generationNo = 1
    while len(fifo) != 0:
        #print(len(fifo))
        newFifo = {}
        for key in fifo:
            exploreNode = simulation["graph"].node[key]
     #       print(exploreNode["descendants"])
            if exploreNode["descendants"] == lastGenerationCount:
                return key, generationNo
            A = exploreNode["parentA"]
            B = exploreNode["parentB"]
            for parent in [A, B]:
                if parent is not None and parent not in newFifo:
                    newFifo[parent] = True
        fifo = newFifo
        generationNo += 1
    return None
