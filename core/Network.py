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

    def getNumOfLinks(self):
        return len(self.m_ListOfLinks)

    def getListOfLinks(self):
        return self.m_ListOfLinks

    def getNumOfDemands(self):
        return len(self.m_ListOfDemands)

    def getListOfDemands(self):
        return self.m_ListOfDemands