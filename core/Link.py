
class Link():
    m_OriginNode = 0
    m_EndNode = 0
    m_Capacity = 0
    m_Cost = 0
    m_LambdasPerFibre = 0

    def __init__(self, originNode, endNode, capacity, cost, lambdasPerFibre):
        self.m_OriginNode = originNode
        self.m_EndNode = endNode
        self.m_Capacity = capacity
        self.m_Cost = cost
        self.m_LambdasPerFibre = lambdasPerFibre