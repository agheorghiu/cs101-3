from interf import *
from helpers import *

numBits = 5

def constant0(x: BinStr) -> int:
    return 0

def constant1(x: BinStr) -> int:
    return 1

def balanced1(x: BinStr) -> int:
    return toInt(x) % 2

def balanced2(x: BinStr) -> int:
    if (toInt(x) < (2**numBits)/2):
        return 0
    return 1

def balanced3(x: BinStr) -> int:
    return 1 - balanced2(x)

def balanced4(x: BinStr) -> int:
    xi = toInt(x)
    if (xi < (2**numBits) / 4):
        return 0
    elif (xi < (2**numBits) / 2):
        return 1
    elif (xi < 3*(2**numBits) / 4):
        return 0
    return 1

