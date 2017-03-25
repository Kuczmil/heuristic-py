#  Requested input:
#  * start population size
#  * probability of crossingover and mutation
#  * choice of seed for psuedorandom number generator
#  * choice of stop criteria (time, number of generations, number of mutations, no improvement in consecutive N generations)
#  * save trajectory to file - sequence of best chromosomes in following generations
#
from core.DAP import DAP as DAP
import core.Network
import random, operator, time


class Evolution():
    m_Population = []
    m_StartPopulationSize = 0
    m_ProbabilityOfCrossingover = 0.0
    m_ProbabilityOfMutation = 0.0
    m_SeedForPseudorandomFunction = 0
    m_ListOfStopCriteria = ['time', 'number_of_generations', 'number_of_mutations', 'no_improvement']
    m_ChosenCriterion = 'time'
    m_ValueOfChosenCriterion = -1
    dap = DAP()

    def __init__(self, startPopulationSize, probabOfCrossingover, probabOfMutation, seed, chosenStopCriterion, valueOfChosenCriterion=-1):
        self.m_StartPopulationSize = startPopulationSize
        self.m_ProbabilityOfCrossingover = probabOfCrossingover
        self.m_ProbabilityOfMutation = probabOfMutation
        self.m_SeedForPseudorandomFunction = seed
        self.m_ChosenCriterion = chosenStopCriterion
        if (valueOfChosenCriterion != -1):
            self.m_ValueOfChosenCriterion = valueOfChosenCriterion
        random.seed(self.m_SeedForPseudorandomFunction)

    def createStartingPopulation(self, network):
        assert type(network) is core.Network.Network, "Lenght of passed network is lower than 1!"
        self.dap = DAP(network)
        for i in range(0, self.m_StartPopulationSize):
            self.m_Population.append(self.dap.createRandomPopulationAndReturnUncheckedResult())

        # print("Population creation finished:")
        # for population in self.m_Population:
        #     print(population)

    def doRoundOfEvolution(self):
        for i in range(0, 5000):
            self.crossingOver()
            self.mutation()
            self.selectNewPopulation()
        self.selectNewPopulation(True)

    def crossingOver(self):
        for i in range(0, len(self.m_Population)):
            pairChromosome = random.randint(0, len(self.m_Population) - 1)
            if pairChromosome == i:
                continue
            elif random.random() > self.m_ProbabilityOfCrossingover:
                continue
            else:
                newChromosome = []
                for gene in range(0, len(self.m_Population[i])):
                    if random.random() > 0.5:
                        newChromosome.append(list(self.m_Population[i][gene]))
                    else:
                        newChromosome.append(list(self.m_Population[pairChromosome][gene]))
                self.m_Population.append(newChromosome)

    def mutation(self):
        for i in range(0, len(self.m_Population)):
            if random.random() < self.m_ProbabilityOfMutation:
                self.m_Population[i] = self.dap.createRandomPopulationAndReturnUncheckedResult()

    def selectNewPopulation(self, final=False):
        costs = self.dap.countCostOfSolution(self.m_Population)
        sortedCosts = sorted(costs.items(), key=operator.itemgetter(1))
        newPopulation = []
        if not final:
            for i in range(0, self.m_StartPopulationSize):
                newPopulation.append(list(self.m_Population[sortedCosts[i][0]]))
            self.m_Population = list(newPopulation)
        else:
            self.saveResult(sortedCosts[0][1])

    def checkIfPopulationCorrect(self):
        pass

    def saveResult(self, bestCost=0):
        nameOfFile = "result_" + time.strftime("%Y%m%d-%H%M%S") + ".txt"
        pathToFile = "../outputs/" + nameOfFile
        with open(pathToFile, 'w') as f:
            f.write("Population size: " + str(self.m_StartPopulationSize) + "\n")
            f.write("Probability of crossingover: " + str(self.m_ProbabilityOfCrossingover) + "\n")
            f.write("Probability of mutation: " + str(self.m_ProbabilityOfMutation) + "\n")
            f.write("Seed for pseudorandom functions: " + str(self.m_SeedForPseudorandomFunction) + "\n")
            f.write("Chosen stop criterion: " + str(self.m_ChosenCriterion) + "\n")
            if self.m_ValueOfChosenCriterion is not -1:
                f.write("Value of chosen criterium: " + str(self.m_ValueOfChosenCriterion) + "\n")

            f.write("\n\n\n")
            f.write("Cost of best chromosome: " + str(bestCost) + "\n")
            i = 0
            for gene in self.m_Population[0]:
                f.write(str(i+1) + ": " + str(gene) + "\n")
                i += 1
