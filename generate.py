from random import seed, random, shuffle, randint, choice
from functools import reduce

def operation(operator):
    """
    A utility function used in order to determine the operation corresponding
    to the operator that is given in string format
    """
    if operator == '+':
        return lambda a, b: a + b
    elif operator == '-':
        return lambda a, b: a - b if a > b else b - a
    elif operator == '*':
        return lambda a, b: a * b
    elif operator == '/':
        return lambda a, b: a / b
    else:
        return None

def adjacent(xy1, xy2):
    """
    Checks wheither two positions represented in 2D coordinates are adjacent
    """
    x1, y1 = xy1
    x2, y2 = xy2
    dx, dy = x1 - x2, y1 - y2
    return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)

def generate(size):
    board = [[((i + j) % size) + 1 for i in range(size)] for j in range(size)]
    for _ in range(size):
        shuffle(board)

    for c1 in range(size):
        for c2 in range(size):
            if random() > 0.5:
                for r in range(size):
                    board[r][c1], board[r][c2] = board[r][c2], board[r][c1]

    board = {(j , i ): board[i][j] for i in range(size) for j in range(size)}
    uncaged = sorted(board.keys(), key=lambda var: var[1])
    grids = []
    while uncaged:
        grids.append([])
        csize = randint(1, 4)
        cell = uncaged[0]
        uncaged.remove(cell)
        grids[-1].append(cell)
        for _ in range(csize - 1):
            adjs = [other for other in uncaged if adjacent(cell, other)]
            cell = choice(adjs) if adjs else None
            if not cell:
                break
            uncaged.remove(cell)
            grids[-1].append(cell)
        csize = len(grids[-1])
        if csize == 1:
            cell = grids[-1][0]
            grids[-1].append(".")
            grids[-1].append(board[cell])
            continue
        elif csize == 2:
            fst, snd = grids[-1][0], grids[-1][1]
            if board[fst] / board[snd] > 0 and not board[fst] % board[snd]:
                operator = "/" # choice("+-*/")
            else:
                operator = "-" # choice("+-*")
        else:
            operator = choice("+*")
        target = reduce(operation(operator), [board[cell] for cell in grids[-1]])
        grids[-1].append(operator)
        grids[-1].append(int(target))
    return size, grids

def format2Gui(n, grid):
    grids_Gui = []
    for lst in grid:
        op, num = lst[-2], lst[-1]
        num_Gui = f'{num}{op}' if op != '.' else str(num)
        points = lst[:-2]
        val = []
        for point in points:
            val.append((point[0])*n+point[1]+1)
        grids_Gui.append([num_Gui, val])
    return n, grids_Gui

def format2Solver(n, g):
    a = []
    for i in range(len(g)):
        s = "["
        op = g[i][-2]
        num = g[i][-1]
        for j in range(len(g[i]) - 2):
            s += str(g[i][j]) + ","
        s = s[0:-1] + "]"
        s = s + " " + op + " " + str(num) + "\n"
        a.append(s)
    return n, a