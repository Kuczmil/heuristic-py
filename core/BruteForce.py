import itertools, math
from core import Network as Network

class BruteForce():
    m_ListOfCombinationsOnSingleDemands = []
    m_Network = Network.Network()
    m_ListOfNumberOfPossibleCombinationsOnDemand = []
    m_ListOfCurrentIteration = []
    isDAP = False
    # variables for DDAP
    m_BestSolution = []
    m_BestSolutionCost = math.inf

    def __init__(self, network, isDAP):
        self.m_Network = network
        self.isDAP = isDAP

    def generateAllPossibleSolutions(self):
        maxNumberOfPaths = 0
        for demand in self.m_Network.m_ListOfDemands:
            listToAppend = self.generatePermutationOnGivenDemand(len(demand.m_ListOfPaths), demand.m_Demand)
            self.m_ListOfCombinationsOnSingleDemands.append(listToAppend)
            self.m_ListOfNumberOfPossibleCombinationsOnDemand.append(len(listToAppend))
            if len(listToAppend) > maxNumberOfPaths:
                maxNumberOfPaths = len(listToAppend)
        for i in range(0, len(self.m_ListOfNumberOfPossibleCombinationsOnDemand)):
            self.m_ListOfCurrentIteration.append(0)

    def generatePermutationOnGivenDemand(self, numberOfPaths, demand):
        allPossibleQuanta = [x for x in range(0, int(demand)+1)]
        return [x for x in itertools.product(allPossibleQuanta, repeat=numberOfPaths) if sum(x) == int(demand)]

    def startBruteforce(self):
        self.generateAllPossibleSolutions()
        totalRange = 1
        for partialRange in self.m_ListOfNumberOfPossibleCombinationsOnDemand:
            totalRange *= int(partialRange)
        for i in range(0, totalRange):
            self.returnNextCombinationToCheck()
            #print(self.m_ListOfCombinationsOnSingleDemands)
            newSolution = []
            for i in range(0, len(self.m_ListOfCurrentIteration)):
                newSolution.append(self.m_ListOfCombinationsOnSingleDemands[i][self.m_ListOfCurrentIteration[i]])
            if self.isDAP:
                if self.checkBruteForceSoultionDAP(newSolution):
                    print("Solution found: ")
                    print(newSolution)
                    break
                else:
                    for link in self.m_Network.getListOfLinks():
                        link.resetCapacityInLambdas()
            else:
                self.countCostOfSolutionDDAP(newSolution)
        if self.isDAP:
            print("Solution not found")
        else:
            print("Best solution - cost and result")
            print(self.m_BestSolutionCost)
            print(self.m_BestSolution)

    def returnNextCombinationToCheck(self, column=0):
        if column == (len(self.m_ListOfNumberOfPossibleCombinationsOnDemand) - 1):
            self.m_ListOfCurrentIteration[column] += 1
            if self.m_ListOfCurrentIteration[column] == self.m_ListOfNumberOfPossibleCombinationsOnDemand[column]:
                self.m_ListOfCurrentIteration[column] = 0
                return True
            else:
                return False
        else:
            if self.returnNextCombinationToCheck(column+1):
                self.m_ListOfCurrentIteration[column] += 1
            if self.m_ListOfCurrentIteration[column] == self.m_ListOfNumberOfPossibleCombinationsOnDemand[column]:
                self.m_ListOfCurrentIteration[column] = 0
                return True
            else:
                return False

    def checkBruteForceSoultionDAP(self, solution):
        solutionColumn = 0
        solutionRow = 0

        for demand in self.m_Network.getListOfDemands():
            for path in demand.m_ListOfPaths:
                for edge in path[1]:
                    properLink = self.m_Network.getListOfLinks()[int(edge) - 1]
                    if not properLink.reduceAvailableCapacity(solution[solutionColumn][solutionRow]):
                        return False

                solutionRow += 1
            solutionRow = 0
            solutionColumn += 1

        return True

    def countCostOfSolutionDDAP(self, solution):
        numOfGene = 0
        numOfAllel = 0
        listOfDemands = self.m_Network.getListOfDemands()
        listOfLinks = self.m_Network.getListOfLinks()
        costsPerEdges = {}

        totalCost = 0
        for gene in solution:
            for allel in gene:
                for edge in listOfDemands[numOfGene].m_ListOfPaths[numOfAllel][1]:
                    if edge not in costsPerEdges:
                        costsPerEdges[edge] = allel
                    else:
                        costsPerEdges[edge] += allel
                numOfAllel += 1
            numOfAllel = 0
            numOfGene += 1
        for edge, usage in costsPerEdges.items():
            realEdge = int(edge) - 1  # Edges are counted from 1, lists from 0
            capacityInLambdas = listOfLinks[realEdge].m_CapacityInLambdas
            costPerFibre = listOfLinks[realEdge].m_Cost
            totalCost += math.ceil(usage / capacityInLambdas) * costPerFibre

        if self.m_BestSolutionCost > totalCost:
            self.m_BestSolutionCost = totalCost
            self.m_BestSolution = list(solution)

        # solutionColumn = 0
        # solutionRow = 0
        # costOfThatSolution = 0
        #
        # for demand in self.m_Network.getListOfDemands():
        #     for path in demand.m_ListOfPaths:
        #         costOfThatSolution += int(solution[solutionColumn][solutionRow]) * float(path[2])
        #         solutionRow += 1
        #     solutionRow = 0
        #     solutionColumn += 1
        # print(costOfThatSolution)
        # if self.m_BestSolutionCost > costOfThatSolution:
        #     self.m_BestSolutionCost = costOfThatSolution
        #     self.m_BestSolution = list(solution)
