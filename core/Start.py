from core import Parser, Problem, DDAP, Evolution
import sys
import os.path

def printSettings(settings):
    for key, value in settings.items():
        print(str(key) + ": " + str(value))

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Not enough arguments are given. Please run script with paths to file with network and input settings")
        # pathToFile = ""
        # while(not os.path.isfile(pathToFile)):
        #     print("Please enter path to input file. To terminate press [N]")
        #     pathToFile = input()
        #     if (pathToFile == "N"):
        #         break
    else:
        pathToFile = sys.argv[1]
        pathToInputSettings = sys.argv[2]

    parser = Parser.Parser(pathToFile, pathToInputSettings)

    if parser.parseNetwork():
        network = parser.returnNetwork()
        network.countTotalUnitCostPerPath()

        settings = parser.returnSettings()
        printSettings(settings)

        populationSize = int(settings['population_size'])
        probabOfCrossingover = float(settings['probab_of_crossingover'])
        probabOfMutation = float(settings['probab_of_mutation'])
        stopCriterion = settings['stop_criterion']
        valueOfStopCriterion = int(settings['value_of_stop_criterion'])
        seed = int(settings['seed'])

        if settings['method'] == 'evolution':
            isDAP = True if (settings['problem'] == 'DAP') else False
            evo = Evolution.Evolution(isDAP, populationSize, probabOfCrossingover, probabOfMutation, seed, stopCriterion, valueOfStopCriterion)
            evo.createStartingPopulation(network)
            evo.startEvolutionAlgorithm()

        elif settings['method'] == 'bruteforce' and settings['problem'] == 'DAP':
            dap = Problem.Problem(network)
            dap.startBruteForce()
            dap.printSolution()

        elif settings['method'] == 'bruteforce' and settings['problem'] == 'DDAP':
            ddap = DDAP.DDAP(network, 100)
            ddap.startBruteForceIterations()

        else:
            print("!!!!!!!!!!!!!!!!!!!!")
            print("SOMETHING WENT WRONG")
            print("!!!!!!!!!!!!!!!!!!!!")
            print("BELOW CORECT INPUT FILE")
            print(parser.exampleOfInputFile)