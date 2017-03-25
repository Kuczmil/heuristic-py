from core import Network
from random import shuffle
import time, math, random

class Problem():
    m_Network = Network.Network()
    m_ListOfLambdasPerLink = []
    m_Solution = []

    def __init__(self, network=Network.Network()):
        self.m_Network = network
        self.initializeListOfLambdasPerLink()

    def initializeListOfLambdasPerLink(self):
        for i in range(0, len(self.m_Network.getListOfLinks())):
            self.m_ListOfLambdasPerLink.append(0)

    def startBruteForce(self):
        areConditionsMet = False
        while(not areConditionsMet):
            self.doBruteForce()
            if self.checkBruteForceSoultion():
                areConditionsMet = True
                return True
            # else:
                #print("Last iteration of brutforce was unsuccessful. New iteration started.")
                # for link in self.m_Network.getListOfLinks():
                #     print(link.m_CapacityInLambdas)

            for link in self.m_Network.getListOfLinks():
                link.resetCapacityInLambdas()
                # print(link.m_CapacityInLambdas)

    def doBruteForce(self):
        lengthOfListOfDemand = len(self.m_Network.getListOfDemands())
        shuffledListOfOrder = [x for x in range(0, lengthOfListOfDemand)]
        shuffle(shuffledListOfOrder)
        dictOfSolutions = {}

        for elementFromShuffledListOfOrder in shuffledListOfOrder:
            demand = self.m_Network.getListOfDemands()[elementFromShuffledListOfOrder]
            demandToFulfill = int(demand.m_Demand)
            listOfLoads = []

            sizeOfListOfPaths = len(demand.m_ListOfPaths)
            for i in range (0, sizeOfListOfPaths):
                listOfLoads.append(0)

            shouldAllDemandBeOnOnePath = False

            if shouldAllDemandBeOnOnePath:
                # method used to add all demand on one path
                pathToAssignLoad = random.randint(0, sizeOfListOfPaths - 1)
                listOfLoads[pathToAssignLoad] += demandToFulfill
            else:
                # method used to add demand on more than one path
                while demandToFulfill != 0:
                    random.seed(time.clock())
                    loadPerGivenPath = random.randint(0, demandToFulfill)
                    loadPerGivenPath %= 5
                    pathToAssignLoad = random.randint(0, sizeOfListOfPaths-1)
                    listOfLoads[pathToAssignLoad] += loadPerGivenPath
                    demandToFulfill -= loadPerGivenPath

            dictOfSolutions[elementFromShuffledListOfOrder] = listOfLoads
        # print(dictOfSolutions)
        for i in range(0, lengthOfListOfDemand):
            self.m_Solution.append(dictOfSolutions[i])
        dictOfSolutions.clear()

    def createRandomPopulationAndReturnUncheckedResult(self):
        self.doBruteForce()
        tempListToReturn = list(self.m_Solution)
        self.m_Solution.clear()
        return tempListToReturn

    def checkBruteForceSoultion(self):
        solutionColumn = 0
        solutionRow = 0

        for demand in self.m_Network.getListOfDemands():
            for path in demand.m_ListOfPaths:
                for edge in path[1]:
                    properLink = self.m_Network.getListOfLinks()[int(edge) - 1]
                    if not properLink.reduceAvailableCapacity(self.m_Solution[solutionColumn][solutionRow]):
                        # print("Edge number: " + edge)
                        self.m_Solution.clear()
                        return False

                solutionRow += 1
            solutionRow = 0
            solutionColumn += 1

        return True

    def countCostOfSolution(self, listOfSolutions=0):
        dictOfCosts = {}
        numOfChromosome = 0
        numOfGene = 0
        numOfAllel = 0
        listOfDemands = self.m_Network.getListOfDemands()
        costsPerEdges = {}
        listOfLinks = self.m_Network.getListOfLinks()

        for chromosome in listOfSolutions:
            totalCost = 0
            for gene in chromosome:
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
                totalCost += math.ceil(2 * usage / capacityInLambdas) * costPerFibre
            dictOfCosts[numOfChromosome] = totalCost
            numOfAllel = 0
            numOfGene = 0
            numOfChromosome += 1
            costsPerEdges.clear()

        return dictOfCosts

    def countCostOfSolutionDAP(self, listOfSolutions=0):
        numberOfChromosome = 0
        dictOfCosts = {}
        totalNumberOfNotfittedLambdas = 0

        for chromosome in listOfSolutions:
            solutionColumn = 0
            solutionRow = 0
            for demand in self.m_Network.getListOfDemands():
                for path in demand.m_ListOfPaths:
                    for edge in path[1]:
                        properLink = self.m_Network.getListOfLinks()[int(edge) - 1]
                        properLink.reduceAvailableCapacity(chromosome[solutionColumn][solutionRow])
                    solutionRow += 1
                solutionRow = 0
                solutionColumn += 1

            for link in self.m_Network.getListOfLinks():
                totalNumberOfNotfittedLambdas += abs(link.m_CapacityInLambdas)
                link.resetCapacityInLambdas()

            dictOfCosts[numberOfChromosome] = totalNumberOfNotfittedLambdas
            totalNumberOfNotfittedLambdas = 0
            numberOfChromosome += 1

        print(dictOfCosts)
        return dictOfCosts


    def printSolution(self):

        print("SOLUTION DAP:")
        maxNumberOfRows = max(len(columnSize) for columnSize in self.m_Solution)
        for i in range(0, maxNumberOfRows):
            lineToPrint = ""
            for j in range(0, len(self.m_Solution)):
                lineToPrint += "|"

                if len(self.m_Solution[j]) > i:
                    lineToPrint += str(self.m_Solution[j][i])
                else:
                    lineToPrint += "-"
            lineToPrint += "|"
            print(lineToPrint)