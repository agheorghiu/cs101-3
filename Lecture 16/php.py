from typing import *
import numpy as np
import random
import functools
import qsharp
from parityHalving import (solvePHP, solveRPHP)

# some helper functions

# dot product of 2 bit strings
def binaryDot(x: List[bool], y: List[bool]) -> bool:
    return functools.reduce(lambda a, b: a ^ b, [(a & b) for (a, b) in zip(x, y)], False)

# convert number to bit string
def toBinary(num: int, numBits: int) -> List[bool]:
    return list(reversed([(num & (2**i)) > 0 for i in range(numBits)]))

# turn list of ints to bools
def toBools(x: List[int]) -> List[bool]:
    return list(map(lambda e: e > 0, x))

# compute parities of neighboring bits for bit string
def computeParities(x: List[bool]) -> List[bool]:
    numBits = len(x)
    parities = []
    for i in range(numBits - 1):
        parities += [(x[i] ^ x[i + 1])]
    return parities


# generate random input for PHP
def generateInput(numBits: int) -> List[bool]:
    x = []
    for i in range(numBits - 1):
        x +=[random.choice([True, False])]
    if (sum(x) % 2 > 0):
        x += [True]
    else:
        x += [False]
    return x

# check whether PHP output is valid
def checkPHPSol(x: List[bool], y: List[bool]) -> bool:
    return ((sum(x) / 2) % 2 == sum(y) % 2)

# check whether RPHP output is valid
def checkRPHPSol(x: List[bool], y: List[bool], parities: List[bool]) -> bool:
    numBits = len(x)
    for i in range(2 ** numBits):
        z = toBinary(i, numBits)
        pz = computeParities(z)
        if (pz == parities and ((sum(x) / 2) + binaryDot(x, z)) % 2 == sum(y) % 2):
            print(z)
            return True
    return False        


x = generateInput(5)
print(list(map(lambda y: int(y), x)))

# run a PHP example
phpSol = solvePHP.simulate(x=x)
print(phpSol)
print(checkPHPSol(x, phpSol))

# run a relaxed PHP example
(y, parities) = solveRPHP.simulate(x=x)
print(y)
print(parities)
print(checkRPHPSol(x, y, parities))