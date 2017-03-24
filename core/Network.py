from core import Link, Demands

class Network():
    m_ListOfLinks = []
    m_ListOfDemands = []

    def __init__(self):
        pass

    def appendToListOfLinks(self, newEntry):
        self.m_ListOfLinks.append(newEntry)

    def appendToListOfDemands(self, newEntry):
        self.m_ListOfDemands.append(newEntry)

    def countTotalUnitCostPerPath(self):
        listOfLinkCosts = []

        for link in self.m_ListOfLinks:
            listOfLinkCosts.append(link.m_Cost/link.m_CapacityInLambdas)

        for demand in self.m_ListOfDemands:
            for path in demand.m_ListOfPaths:
                totalCost = 0
                for link in path[1]:
                    totalCost += listOfLinkCosts[int(link)-1]
                path[2] = totalCost

    def getNumOfLinks(self):
        return len(self.m_ListOfLinks)

    def getListOfLinks(self):
        return self.m_ListOfLinks

    def getNumOfDemands(self):
        return len(self.m_ListOfDemands)

    def getListOfDemands(self):
        return self.m_ListOfDemands