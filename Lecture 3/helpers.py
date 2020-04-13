import functools
from sage import *
from interf import *

numBits = 5

# Gaussian elimination

# swap elements in list
def swap(list, i, j):
    list[i], list[j] = list[j], list[i]
    return list

# perform backwards substitution
def backwards(list, solution):
    final = solution[0]
    param = len(list)
    for i in range(param - 1, -1, -1):
        sol = final * list[i][param]
        for j in range(1, param - i):
            sol = (sol + (list[i][i + j] * solution[j - 1])) % 2
        if (list[i][i] == 0):
            if (sol == 1):
                return False
            else:
                solution = [1] + solution
        else:
            solution = [sol] + solution
    return solution

# Gaussian elimination
def gauss(list):
    #since this is for Simon's problem, assume the matrix is n-1 x n
    n = len(list)
    #loop over the pivots
    for i in range(0, n):
    #now find index of first 1 in column i
        max = i
        for k in range(i, n):
            if (list[k][i] == 1):
                max = k
                break
    # now do a swap then take away row from other rows (if there is a 1 in the element)
        if (list[max][i] == 1):
            swap(list, i, max)
            for u in range(i+1, n):
                if (list[u][i] == 1):
                    for v in range(0, n + 1):
                        list[u][v] = (list[u][v] + list[i][v]) % 2
    # now check there are no rows of all zeroes
    for i in range(0, n):
        count = 0
        for j in range(0, n + 1):
            if (list[i][j] == 0):
                count += 1
        if (count == n + 1):
            return "no solution!"
    # now check there are no columns of all zeroes
    for i in range(0, n + 1):
        count = 0
        for j in range(0, n):
            if (list[j][i] == 0):
                count += 1
        if (count == n + 1):
            return "no solution!"
    # now do some back substitution
    if (backwards(list, [1]) == False):
        return backwards(list, [0])

    return backwards(list, [1])

# binary arithmetic helper functions
def binaryDot(x: BinStr, y: BinStr) -> bool:
    return functools.reduce(lambda a, b: a ^ b, [(a & b) for (a, b) in zip(x, y)], False)

def binaryAdd(x: BinStr, y: BinStr) -> BinStr:
    return [(a ^ b) for (a, b) in zip(x, y)]

def isOrthToAll(x: BinStr, vects: List[BinStr]):
    return functools.reduce(lambda a, b: a & b, list(map(lambda c: binaryDot(x, c), vects)), True)

# converting between binary and int
def toBinary(num: int) -> BinStr:
    return list(reversed([(num & (2**i)) > 0 for i in range(numBits)]))

def toInt(x: BinStr) -> int:
    rx = list(reversed(x))
    return sum([rx[i]*(2**i) for i in range(len(rx))])

# rotate list
def rotate(l, n):
    return l[n:] + l[:n]

# wrapper function to be used for interf
def wrapperFun(f: Callable[[BinStr], bool]) -> Callable[[BinStr], int]:
    return (lambda x: (-1)**f(x))


