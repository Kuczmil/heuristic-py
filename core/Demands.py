
class Demands:
    # m_ListOfPaths structure (number of path, list of used edges, total unit cost of that path)
    m_ListOfPaths = []
    m_OriginNode = 0
    m_EndNode = 0
    m_Demand = 0
    m_NumberOfPaths = 0

    def __init__(self, originNode, endNode, demand, numberOfPaths):
        self.m_ListOfPaths = []
        self.m_OriginNode = originNode
        self.m_EndNode = endNode
        self.m_Demand = demand
        self.m_NumberOfPaths = numberOfPaths

    def addToListOfPaths(self, numOfPath, listOfUsedEdges):
        # print("List of used edges: " + str(listOfUsedEdges))
        self.m_ListOfPaths.append([numOfPath, listOfUsedEdges, 0])