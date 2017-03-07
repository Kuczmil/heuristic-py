
class Link():
    m_OriginNode = 0
    m_EndNode = 0
    m_Capacity = 0              # capacity in fibres per link
    m_Cost = 0
    m_LambdasPerFiber = 0       # lambdas per fiber
    m_CapacityInLambdas = 0

    def __init__(self, originNode, endNode, capacity, cost, lambdasPerFiber):
        self.m_OriginNode = originNode
        self.m_EndNode = endNode
        self.m_Capacity = capacity
        self.m_Cost = cost
        self.m_LambdasPerFiber = lambdasPerFiber
        self.resetCapacityInLambdas()

    def reduceAvailableCapacity(self, usedLambdas):
        self.m_CapacityInLambdas -= usedLambdas
        if (self.m_CapacityInLambdas >= 0):
            return True
        else:
            return False

    def resetCapacityInLambdas(self):
        self.m_CapacityInLambdas = int(self.m_LambdasPerFiber) * int(self.m_Capacity)