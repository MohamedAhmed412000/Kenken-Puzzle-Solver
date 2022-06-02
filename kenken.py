import re
import sys

def removeSpace(l):
    ind = l.find(']')
    remain = l[ind:-1]
    l = l[0:ind]
    for i in range(len(l)):
        if i >= len(l) or l[i] == ']':
            break
        if l[i - 1] == ',' and l[i] == ' ' and i != 0:
            l = l.replace(l[i],'')
    l += remain
    return l.split()

class KenKen():

    def __init__(self, size, lines):
        self.variables = list()
        self.neighbors = dict()
        self.blockVar = list()
        self.blockOp = list()
        self.blockValue = list()
        self.blockVariables = list()

        """Create variables list"""
        for i in range(size):
            for j in range(size):
                self.variables.append('K' + str(i) + str(j))

        """Create domains dictionary"""
        dictDomainsValues = list(range(1, size + 1))
        self.domains = dict((v, dictDomainsValues) for v in self.variables)

        """Create neighbors dictionary"""
        for v in self.variables:
            dictNeighborValue = []
            coordinateX = int(list(v)[1])
            coordinateY = int(list(v)[2])

            for i in range(size):
                if i != coordinateY:
                    string = 'K' + str(coordinateX) + str(i)
                    dictNeighborValue.append(string)
                if i != coordinateX:
                    string = 'K' + str(i) + str(coordinateY)
                    dictNeighborValue.append(string)

            self.neighbors[v] = dictNeighborValue

        """Create constraint data lists"""
        for l in lines:
            var, op, val = removeSpace(l)

            self.blockVar.append(re.findall('\d+', var))
            self.blockOp.append(op)
            self.blockValue.append(int(val))

        for i in range(len(self.blockVar)):
            blockList = []
            for j in range(0, len(self.blockVar[i]), 2):
                string = 'K' + str(self.blockVar[i][j]) + str(self.blockVar[i][j + 1])
                blockList.append(string)

            self.blockVariables.append(blockList)
    
    def add_CSP(self, csp):
        self.game_kenken = csp