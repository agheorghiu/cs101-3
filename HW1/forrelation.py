from interf import *
from helpers import *

numBits = 5
domain = list(map(lambda x: toBinary(x, numBits), range(2**numBits)))

# forrelated pairs (all the pairs below should yield a high Phi value)
# note that these pairs are only forrelated for numBits <= 5
def f1(x: BinStr) -> int:
    v = [1, 1, -1, 1, -1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, 1, -1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1]
    return v[toInt(x) % 32]

def g1(x: BinStr) -> int:
    S = 0
    for y in domain:
        S += f1(y) * (-1)**binaryDot(x, y)
    if (S > 0):
        return 1
    return -1


def f2(x: BinStr) -> int:
    if (toInt(x) % 6 == 0):
        return -1
    if (toInt(x) % 4 == 0):
        return -1
    if (toInt(x) % 3 == 0):
        return -1
    return 1

def g2(x: BinStr) -> int:
    S = 0
    for y in domain:
        S += f2(y) * (-1)**binaryDot(x, y)
    if (S > 0):
        return 1
    return -1



# un-forrelated pairs (all the pairs below should yield a low Phi value)
def f3(x: BinStr) -> int:
    return (-1)**hammingWeight(x)

def g3(x: BinStr) -> int:
    return 1


def f4(x: BinStr) -> int:
    return 1

def g4(x: BinStr) -> int:
    val = 0
    for y in domain:
        val += f4(y) * (-1)**binaryDot(x, y)
    val = abs(val) / 2**numBits
    return (-1)**val


def f5(x: BinStr) -> int:
    return random.choice([-1, 1])

def g5(x: BinStr) -> int:
    return random.choice([-1, 1])


# non-forrelated (Phi is in between 1/3 and 2/3)
def f6(x: BinStr) -> int:
    if (toInt(x) < 2**(numBits/ 2)):
        return 1
    return (-1)**toInt(x)

def g6(x: BinStr) -> int:
    return f6(x)
