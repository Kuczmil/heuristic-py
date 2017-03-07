from core import Network
import random

class DAP():
    m_Network = Network.Network()
    m_ListOfLambdasPerLink = []
    m_Solution = []

    def __init__(self, network):
        self.m_Network = network
        self.initializeListOfLambdasPerLink()


    def initializeListOfLambdasPerLink(self):
        for i in range(0, len(self.m_Network.getListOfLinks())):
            self.m_ListOfLambdasPerLink.append(0)

    def startBruteForce(self):

        for demand in self.m_Network.getListOfDemands():
            demandToFulfill = int(demand.m_Demand)
            listOfLoads = []

            sizeOfListOfPaths = len(demand.m_ListOfPaths)
            for i in range (0, sizeOfListOfPaths):
                listOfLoads.append(0)

            while demandToFulfill != 0:
                loadPerGivenPath = random.randint(0, demandToFulfill)
                pathToAssignLoad = random.randint(0, sizeOfListOfPaths-1)
                listOfLoads[pathToAssignLoad] += loadPerGivenPath
                demandToFulfill -= loadPerGivenPath

            # This part of code is wrong since we do not check whether all demand is assigned
            # Also first paths have higher probability that larger load will be assigned to them
            # for path in demand.m_ListOfPaths:
            #     if (demandToFulfill > 0):
            #         loadPerGivenPath = random.randint(0, demandToFulfill)
            #         demandToFulfill -= loadPerGivenPath
            #         listOfLoads.append(loadPerGivenPath)
            #     else:
            #         listOfLoads.append(0)

            self.m_Solution.append(listOfLoads)

        if self.checkBruteForceSoultion():
            for link in self.m_Network.getListOfLinks():
                link.resetCapacityInLambdas()
            return True
        else:
            #print("Last iteration of brutforce was unsuccessful. New iteration started.")
            for link in self.m_Network.getListOfLinks():
                link.resetCapacityInLambdas()
            self.startBruteForce()

    def checkBruteForceSoultion(self):
        solutionColumn = 0
        solutionRow = 0

        for demand in self.m_Network.getListOfDemands():
            for path in demand.m_ListOfPaths:
                for edge in path[1]:
                    properLink = self.m_Network.getListOfLinks()[int(edge) - 1]
                    if not properLink.reduceAvailableCapacity(self.m_Solution[solutionColumn][solutionRow]):
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