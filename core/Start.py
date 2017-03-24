from core import Parser, DAP, DDAP, Evolution
import sys
import os.path

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        pathToFile = ""
        while(not os.path.isfile(pathToFile)):
            print("Please enter path to input file. To terminate press [N]")
            pathToFile = input()
            if (pathToFile == "N"):
                break
    else:
        pathToFile = sys.argv[1]

    parser = Parser.Parser(pathToFile)
    if parser.parseNetwork():
        network = parser.returnNetwork()
        network.countTotalUnitCostPerPath()

        evo = Evolution.Evolution(1000, 0.5, 0.05, 1, 'time')
        evo.createStartingPopulation(network)
        evo.doRoundOfEvolution()
        # dap = DAP.DAP(network)
        # dap.startBruteForce()
        # dap.printSolution()
        #
        # ddap = DDAP.DDAP(network, 100)
        # ddap.startBruteForceIterations()

