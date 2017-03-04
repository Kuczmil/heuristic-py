import sys
from core import Link, Demands, Network

class Parser():
    m_Separator = -1
    network = Network.Network()

    def __init__(self, pathToFile):
        with open(pathToFile, 'r') as f:
            m_DataFromFile = f.read()
        self.m_ParsedFile = m_DataFromFile.split("\n")

    def getLineFromParseFile(self):
        for line in self.m_ParsedFile:
            yield line

    def parseNetwork(self):
        self.yielder = self.getLineFromParseFile()
        self.parseLinks()
        self.parseDemands()
        return True

    def parseLinks(self):
        numberOfLinks =  int(self.yielder.__next__())
        print("Declared number of links in network: " + str(numberOfLinks))

        for link in range(0, numberOfLinks):
            inputLine = self.yielder.__next__().split(" ")
            self.network.appendToListOfLinks(Link.Link(*inputLine))

        print("Number of links read: " + str(self.network.getNumOfLinks()))

        assert self.network.getNumOfLinks() == numberOfLinks, "Number of read links is not equal to declared number of links"
        assert self.yielder.__next__() != self.m_Separator, "Corrupted file, separator not present"

    def parseDemands(self):
        numberOfDemands = self.yielder.__next__()
        while(len(numberOfDemands) == 0):
            numberOfDemands = self.yielder.__next__()

        print("Declared number of demands in network: " + numberOfDemands)

        for demand in range(0, int(numberOfDemands)):
            firstLineOfDemands = self.yielder.__next__()
            while (len(firstLineOfDemands) == 0):
                firstLineOfDemands = self.yielder.__next__()
            firstLineOfDemands = firstLineOfDemands.split(" ")
            originNode = firstLineOfDemands[0]
            endNode = firstLineOfDemands[1]
            demand = firstLineOfDemands[2]
            numberOfPaths = int(self.yielder.__next__())
            newDemand = Demands.Demands(originNode, endNode, demand, numberOfPaths)
            for path in range(0, numberOfPaths):
                newPath = self.yielder.__next__().split(" ")
                newDemand.addToListOfDemands(int(newPath[0]), newPath[1:-1])
            self.network.appendToListOfDemands(newDemand)

        print("Number of demands read: " + str(self.network.getNumOfDemands()))

        assert self.network.getNumOfDemands() == int(numberOfDemands), "Number of read demands is not equal to declared number of demands"

    def returnNetwork(self):
        return self.network

if __name__ == '__main__':
    print(str(sys.argv))
    parser = Parser(sys.argv[1])
    parser.parseNetwork()
