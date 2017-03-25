import sys
from core import Link, Demands, Network

class Parser():
    m_Separator = -1
    network = Network.Network()
    m_MeaningfulStrings = ['method', 'problem', 'population_size', 'probab_of_crossingover', 'probab_of_mutation', 'stop_criterion', 'value_of_stop_criterion', 'seed']
    m_DictOfSettings = {}

    def __init__(self, pathToFile, pathToInputSettings):
        with open(pathToFile, 'r') as f:
            m_DataFromFile = f.read()
        self.m_ParsedFile = m_DataFromFile.split("\n")

        with open(pathToInputSettings, 'r') as g:
            m_SettingsFromFile = g.read()
        self.m_ParsedSettings = m_SettingsFromFile.split("\n")

    def getLineFromParseFile(self):
        for line in self.m_ParsedFile:
            yield line

    def parseNetwork(self):
        self.yielder = self.getLineFromParseFile()
        self.parseLinks()
        self.parseDemands()
        self.parseSettings()
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
                newPathBeforeSplit = self.yielder.__next__().strip()
                newPath = newPathBeforeSplit.split(" ")
                # print(newPath)
                newDemand.addToListOfPaths(int(newPath[0]), newPath[1:len(newPath)])
            self.network.appendToListOfDemands(newDemand)

        print("Number of demands read: " + str(self.network.getNumOfDemands()))

        assert self.network.getNumOfDemands() == int(numberOfDemands), "Number of read demands is not equal to declared number of demands"

    def parseSettings(self):
        for line in self.m_ParsedSettings:
            if len(line) == 0 or line[0] == "#":
                continue
            else:
                splitedLine = line.split("=")
                if splitedLine[0] in self.m_MeaningfulStrings:
                    self.m_DictOfSettings[splitedLine[0]] = splitedLine[1]

    def returnNetwork(self):
        return self.network

    def returnSettings(self):
        if (len(self.m_DictOfSettings) != 8):
            print("#####################################################")
            print("CORRUPTED INPUT SETTINGS. EXAMPLARY INPUT FILE BELOW:")
            print("#####################################################")
            print(self.exampleOfInputFile)
        return self.m_DictOfSettings

    exampleOfInputFile = "# brutforce or evolution \nmethod=evolution\n\n# DAP or DDAP\nproblem=DDAP\n\n# size of population\npopulation_size=100\n\n# probability of crossingover - float between 0.0 and 1.0\nprobab_of_crossingover=0.4\n\n# probability of mutation - float between 0.0 and 1.0\nprobab_of_mutation=0.0.5\n\n# stop criterion - one within ['time', 'number_of_generations', 'number_of_mutations', 'no_improvement']\nstop_criterion=number_of_generations\n\n# value of stop criterion\nvalue_of_stop_criterion=1000\n\n# seed (integer)\nseed=123121"

if __name__ == '__main__':
    print(str(sys.argv))
    parser = Parser(sys.argv[1])
    parser.parseNetwork()
