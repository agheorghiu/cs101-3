from typing import *
import random

def interf1(fun: Callable[[Any], int], domain: List[Any], norm: int) -> bool:
    res = sum(map(fun, domain)) / norm
    if (abs(res) >= 2/3):
        return True
    elif (abs(res) <= 1/3):
        return False
    return random.choice([True, False])

def toInt(x: List[bool]) -> int:
    return sum([x[i]*(2**i) for i in range(len(x))])

def oracleFun(n: int, x: int) -> int:
    return (-1) ** ((x == n) - 1)

# deciding whether a solution exists or not using interference (showing UP contained in AWPP)
def interfSearch(fun: Callable[[Any], int], numBits: int) -> bool:
    domain = range(2 ** numBits)
    newDomain = [(x, y) for x in domain for y in domain]

    def newFun(pair):
        x = pair[0]
        y = pair[1]
        if (fun(x) == -1):
            return (-1) ** (y % 2)
        else:
            return 1
    
    return interf1(newFun, newDomain, 2 ** numBits)

# using interfSearch to find the solution when it exists
def findSol(fun: Callable[[Any], int], numBits: int) -> int:
    sol = []

    # use interfSearch to determine each bit of the solution
    for i in range(numBits):
        suffix = toInt(sol)

        # guess for current bit is 0
        domain = map(lambda x: x * (2 ** (i + 1)) + suffix, range(2 ** (numBits - i - 1)))
        newDomain = [(x, y) for x in domain for y in range(2 ** numBits)]

        def newFun(pair):
            x = pair[0]
            y = pair[1]
            if (fun(x) == -1):
                return (-1) ** (y % 2)
            else:
                return 1
    
        # use interfSearch to see if guess is correct
        if (interf1(newFun, newDomain, 2 ** numBits)):
            sol += [0]
        else:
            sol += [1]

    return toInt(sol)

numBits = 5
n = 7

print(interfSearch(lambda x: oracleFun(n, x), numBits))
print(interfSearch(lambda x: -1, numBits))

print(findSol(lambda x: oracleFun(n, x), numBits))
