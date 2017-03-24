#  Requested input:
#  * start population size
#  * probability of crossingover and mutation
#  * choice of seed for psuedorandom number generator
#  * choice of stop criteria (time, number of generations, number of mutations, no improvement in consecutive N generations)
#  * save trajectory to file - sequence of best chromosomes in following generations
#
from core.DAP import DAP as DAP
import core.Network
import random, operator


class Evolution():
    m_Population = []
    m_StartPopulationSize = 0
    m_ProbabilityOfCrossingover = 0.0
    m_ProbabilityOfMutation = 0.0
    m_SeedForPseudorandomFunction = 0
    m_ListOfStopCriteria = ['time', 'number_of_generations', 'number_of_mutations', 'no_improvement']
    m_ChosenCriterium = 'time'
    m_ValueOfChosenCriterium = -1
    dap = DAP()

    def __init__(self, startPopulationSize, probabOfCrossingover, probabOfMutation, seed, chosenStopCriterium, valueOfChosenCriterium=-1):
        self.m_StartPopulationSize = startPopulationSize
        self.m_ProbabilityOfCrossingover = probabOfCrossingover
        self.m_ProbabilityOfMutation = probabOfMutation
        self.m_SeedForPseudorandomFunction = seed
        self.m_ChosenCriterium = chosenStopCriterium
        if (valueOfChosenCriterium != -1):
            self.m_ValueOfChosenCriterium = valueOfChosenCriterium
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
        for i in range(0, 100):
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
            print(sortedCosts)
            print(self.m_Population[0])

    def checkIfPopulationCorrect(self):
        pass