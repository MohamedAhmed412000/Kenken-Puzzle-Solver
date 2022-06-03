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

def kenken_constraint(self, A, a, B, b):
        if B in self.neighbors[A] and a == b:
            return False

        for n in self.neighbors[A]:
            if n in self.game_kenken.infer_assignment() and self.game_kenken.infer_assignment()[n] == a:
                return False

        for n in self.neighbors[B]:
            if n in self.game_kenken.infer_assignment() and self.game_kenken.infer_assignment()[n] == b:
                return False

        blockA = blockB = 0

        for i in range(len(self.blockVariables)):
            if A in self.blockVariables[i]:
                blockA = i
            if B in self.blockVariables[i]:
                blockB = i

        if blockA == blockB:
            blockNum = blockA
            if self.blockOp[blockNum] == '.':
                if A != B:
                    return False
                elif a != b:
                    return False
                elif a != self.blockValue[blockNum]:
                    return False

                return True

            elif self.blockOp[blockNum] == '+':
                sum = assigned = 0

                for v in self.blockVariables[blockNum]:
                    if v == A:
                        sum += a
                        assigned += 1
                    elif v == B:
                        sum += b
                        assigned += 1
                    elif v in self.game_kenken.infer_assignment():
                        sum += self.game_kenken.infer_assignment()[v]
                        assigned += 1

                if sum == self.blockValue[blockNum] and assigned == len(self.blockVariables[blockNum]):
                    return True
                elif sum < self.blockValue[blockNum] and assigned < len(self.blockVariables[blockNum]):
                    return True
                else:
                    return False

            elif self.blockOp[blockNum] == '*':
                sum = 1
                assigned = 0

                for v in self.blockVariables[blockNum]:
                    if v == A:
                        sum *= a
                        assigned += 1
                    elif v == B:
                        sum *= b
                        assigned += 1
                    elif v in self.game_kenken.infer_assignment():
                        sum *= self.game_kenken.infer_assignment()[v]
                        assigned += 1

                if sum == self.blockValue[blockNum] and assigned == len(self.blockVariables[blockNum]):
                    return True
                elif sum <= self.blockValue[blockNum] and assigned < len(self.blockVariables[blockNum]):
                    return True
                else:
                    return False

            elif self.blockOp[blockNum] == '/':
                return max(a, b) / min(a, b) == self.blockValue[blockNum]

            elif self.blockOp[blockNum] == '-':
                return max(a, b) - min(a, b) == self.blockValue[blockNum]

        else:
            constraintA = self.kenken_constraint_op(A, a, blockA)
            constraintB = self.kenken_constraint_op(B, b, blockB)

            return constraintA and constraintB
        
    def kenken_constraint_op(self, var, val, blockNum):
        if self.blockOp[blockNum] == '.':
            return val == self.blockValue[blockNum]
    
        elif self.blockOp[blockNum] == '+':
            sum2 = 0
            assigned2 = 0
    
            for v in self.blockVariables[blockNum]:
                if v == var:
                    sum2 += val
                    assigned2 += 1
                elif v in self.game_kenken.infer_assignment():
                    sum2 += self.game_kenken.infer_assignment()[v]
                    assigned2 += 1
    
            if sum2 == self.blockValue[blockNum] and assigned2 == len(self.blockVariables[blockNum]):
                return True
            elif sum2 < self.blockValue[blockNum] and assigned2 < len(self.blockVariables[blockNum]):
                return True
            else:
                return False
    
        elif self.blockOp[blockNum] == '*':
            sum2 = 1
            assigned2 = 0
    
            for v in self.blockVariables[blockNum]:
                if v == var:
                    sum2 *= val
                    assigned2 += 1
                elif v in self.game_kenken.infer_assignment():
                    sum2 *= self.game_kenken.infer_assignment()[v]
                    assigned2 += 1
    
            if sum2 == self.blockValue[blockNum] and assigned2 == len(self.blockVariables[blockNum]):
                return True
            elif sum2 <= self.blockValue[blockNum] and assigned2 < len(self.blockVariables[blockNum]):
                return True
            else:
                return False
    
        elif self.blockOp[blockNum] == '/':
            for v in self.blockVariables[blockNum]:
                if v != var:
                    constraintVar2 = v
    
            if constraintVar2 in self.game_kenken.infer_assignment():
                constraintVal2 = self.game_kenken.infer_assignment()[constraintVar2]
                return max(constraintVal2, val) / min(constraintVal2, val) == self.blockValue[blockNum]
            else:
                for d in self.game_kenken.choices(constraintVar2):
                    if max(d, val) / min(d, val) == self.blockValue[blockNum]:
                        return True
    
                return False
    
        elif self.blockOp[blockNum] == '-':
            for v in self.blockVariables[blockNum]:
                if v != var:
                    constraintVar2 = v
    
            if constraintVar2 in self.game_kenken.infer_assignment():
                constraintVal2 = self.game_kenken.infer_assignment()[constraintVar2]
                return max(constraintVal2, val) - min(constraintVal2, val) == self.blockValue[blockNum]
            else:
                for d in self.game_kenken.choices(constraintVar2):
                    if max(d, val) - min(d, val) == self.blockValue[blockNum]:
                        return True
    
                return False    

    def display(self, dic, size):
        for i in range(size):
            for j in range(size):
                string = 'K' + str(i) + str(j)
                sys.stdout.write(str(dic[string]) + " ")
            print()

    def format_soln(self, dic, size):
        soln = []
        for i in range(size):
            sub = []
            for j in range(size):
                string = 'K' + str(i) + str(j)
                sub.append(dic[string])
            soln.append(sub)
        return soln
