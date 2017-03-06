from core import Parser, DAP, DDAP
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
        dap = DAP.DAP(network)
        dap.startBruteForce()
        dap.printSolution()

        ddap = DDAP.DDAP(network, 10000)
        ddap.startBruteForceIterations()

