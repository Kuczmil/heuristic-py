from core import Network
import random
from random import shuffle
import time

class DAP():
    m_Network = Network.Network()
    m_ListOfLambdasPerLink = []
    m_Solution = []
    numberOfDDD = 0

    def __init__(self, network):
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
                self.numberOfDDD = 0
                areConditionsMet = True
                return True
            else:
                #print("Last iteration of brutforce was unsuccessful. New iteration started.")
                if (self.numberOfDDD%1000 == 0):
                    print(self.numberOfDDD)
                # for link in self.m_Network.getListOfLinks():
                #     print(link.m_CapacityInLambdas)

                self.numberOfDDD += 1
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

            while demandToFulfill != 0:
                random.seed(time.clock())
                loadPerGivenPath = random.randint(0, demandToFulfill)
                loadPerGivenPath %= 2
                pathToAssignLoad = random.randint(0, sizeOfListOfPaths-1)
                listOfLoads[pathToAssignLoad] += loadPerGivenPath
                demandToFulfill -= loadPerGivenPath

            dictOfSolutions[elementFromShuffledListOfOrder] = listOfLoads
        # print(dictOfSolutions)
        for i in range(0, lengthOfListOfDemand):
            self.m_Solution.append(dictOfSolutions[i])
        dictOfSolutions.clear()
        #
        # if self.checkBruteForceSoultion():
        #     self.numberOfDDD = 0
        #     for link in self.m_Network.getListOfLinks():
        #         link.resetCapacityInLambdas()
        #     return True
        # else:
        #     print("Last iteration of brutforce was unsuccessful. New iteration started.")
        #     for link in self.m_Network.getListOfLinks():
        #         link.resetCapacityInLambdas()
        #     self.startBruteForce()


    def checkBruteForceSoultion(self):
        solutionColumn = 0
        solutionRow = 0

        for demand in self.m_Network.getListOfDemands():
            for path in demand.m_ListOfPaths:
                for edge in path[1]:
                    properLink = self.m_Network.getListOfLinks()[int(edge) - 1]
                    if not properLink.reduceAvailableCapacity(self.m_Solution[solutionColumn][solutionRow]):
                        print("Edge number: " + edge)
                        self.m_Solution.clear()
                        return False

                solutionRow += 1
            solutionRow = 0
            solutionColumn += 1

        return True

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