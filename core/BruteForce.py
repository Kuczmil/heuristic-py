import itertools
from core import Network as Network

class BruteForce():
    m_ListOfAllPossibleSolutions = []
    m_Network = Network.Network()

    def __init__(self, network):
        self.m_Network = network

    def generateAllPossibleSolutions(self):
        maxNumberOfPaths = 0
        listOfCombinationsOnSingleDemands = []
        for demand in self.m_Network.m_ListOfDemands:
            listToAppend = self.generatePermutationOnGivenDemand(len(demand.m_ListOfPaths), demand.m_Demand)
            listOfCombinationsOnSingleDemands.append(listToAppend)
            if len(listToAppend) > maxNumberOfPaths:
                maxNumberOfPaths = len(listToAppend)

        print(listOfCombinationsOnSingleDemands)
        print(maxNumberOfPaths)
        print(len(listOfCombinationsOnSingleDemands))
        #print([x for x in itertools.product([y for y in range(0, maxNumberOfPaths)], repeat=len(self.m_Network.m_ListOfDemands))])
        # allPossiblePathsNames =

        # self.m_ListOfAllPossibleSolutions = [x for x in itertools.product(listOfCombinationsOnSingleDemands, repeat=len(listOfCombinationsOnSingleDemands))]

    def generatePermutationOnGivenDemand(self, numberOfPaths, demand):
        allPossibleQuanta = [x for x in range(0, int(demand)+1)]
        return [x for x in itertools.product(allPossibleQuanta, repeat=numberOfPaths) if sum(x) == int(demand)]

