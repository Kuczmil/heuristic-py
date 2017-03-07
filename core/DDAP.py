from core import DAP
import math

class DDAP(DAP.DAP):
    m_CostOfBestSolution = math.inf
    m_BestSolution = []
    m_NumberOfRounds = 0

    def __init__(self, network, numberOfRounds):
        self.m_Network = network
        self.m_NumberOfRounds = numberOfRounds
        self.m_BestSolution = []

    def startBruteForceIterations(self):
        for i in range(0, self.m_NumberOfRounds):
            self.startBruteForce()
            self.countCostOfSolution()

        self.printSolution()


    def countCostOfSolution(self):
        solutionColumn = 0
        solutionRow = 0
        costOfThatSolution = 0

        for demand in self.m_Network.getListOfDemands():
            for path in demand.m_ListOfPaths:
                costOfThatSolution += int(self.m_Solution[solutionColumn][solutionRow]) * int(path[2])
                solutionRow += 1
            solutionRow = 0
            solutionColumn += 1

        if self.m_CostOfBestSolution > costOfThatSolution:
            self.m_CostOfBestSolution = costOfThatSolution
            self.m_BestSolution = list(self.m_Solution)
        self.m_Solution.clear()

    def printSolution(self):
        print("SOLUTION DDAP:")
        maxNumberOfRows = max(len(columnSize) for columnSize in self.m_BestSolution)
        for i in range(0, maxNumberOfRows):
            lineToPrint = ""
            for j in range(0, len(self.m_BestSolution)):
                lineToPrint += "|"

                if len(self.m_BestSolution[j]) > i:
                    lineToPrint += str(self.m_BestSolution[j][i])
                else:
                    lineToPrint += "-"
            lineToPrint += "|"
            print(lineToPrint)
        print("The best cost is " + str(self.m_CostOfBestSolution))


